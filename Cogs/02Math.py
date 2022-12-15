import discord
from discord.ext import commands
from discord.commands import Option
import config
import utils

embedcolor = config.BOT.embedcolor
warncolor = config.BOT.warncolor


class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="미분", description="미지수가 1개인 f(x)를 미분")
    @commands.max_concurrency(3, commands.BucketType.default)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def derivative(
        self,
        ctx,
        coefficients: str,
        x: Option(int, "미분계수를 구할 경우만 입력", name="x", default=None),
    ):
        try:
            f_x = coefficients
            if coefficients[0] == "x":
                coefficients = "1" + coefficients
            coefficients = sorted(
                [
                    [int(j[1:] if j[0] == "^" else j) for j in i.split("x") if "x" in i]
                    for i in coefficients.replace(" ", "")
                    .replace("-", "+-")
                    .replace("+x", "+1x")
                    .replace("-x", "-1x")
                    .replace("x+", "x^1+")
                    .split("+")
                ],
                key=lambda i: 0 if len(i) != 2 else i[1],
                reverse=True,
            )
            if coefficients[-1] == []:
                del coefficients[-1]
            if coefficients[-1][1] > 10:
                if x is not None:
                    embed = discord.Embed(
                        title="⚠️ 명령어 사용 제한",
                        description="10차 방정식 이상은 미분계수 계산이 제한되었습니다",
                        color=warncolor,
                    )
                    await ctx.respond(embed=embed)
                    return
            if len(coefficients) > 20:
                embed = discord.Embed(
                    title="⚠️ 명령어 사용 제한",
                    description="항은 20개 이상 입력 불가합니다",
                    color=warncolor,
                )
            data = []
            for i in coefficients:
                data.append([i[0] * i[1], i[1] - 1])
            f_prime_x = (
                " + ".join(
                    sorted(
                        [f"{i[0]}x^{i[1]}" for i in data],
                        key=lambda i: i[1] if len(i) == 2 else 0,
                    )
                )
                .replace("+ -", "-")
                .replace("1x", "x")
                .replace("^1", "")
                .replace("x^0", "")
            )
            embed = discord.Embed(title="미분 결과", color=embedcolor)
            embed.add_field(name="f(x)", value=f_x, inline=False)
            embed.add_field(
                name="f`(x)",
                value=f_prime_x[1:] if f_prime_x[0] == "+" else f_prime_x,
                inline=False,
            )
            if x is not None:
                result = 0
                for i in data:
                    result += i[0] * (x ** i[1])
                embed.add_field(name=f"f`({x})", value=str(result), inline=False)
            await ctx.respond(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="수식 입력 방법", color=warncolor)
            embed.add_field(name="미지수 사용", value="> 미지수는 x 1개만 사용 가능합니다", inline=False)
            embed.add_field(
                name="거듭제곱 표현", value="> 거듭제곱은 ^ 뒤에 제곱할 숫자를 입력하셔야 합니다", inline=False
            )
            await ctx.respond(embed=embed)
            print(e)
            raise utils.ReportError


def setup(bot):
    bot.add_cog(Math(bot))
