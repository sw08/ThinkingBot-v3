import discord
from discord.ext import commands
from discord.commands import Option
import config
import utils.math
import utils.errors as errors

embedcolor = config.BOT.embedcolor
warncolor = config.BOT.warncolor


class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="미분", description="미지수가 1개인 f(x)를 미분")
    @commands.max_concurrency(3)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def derivative(
        self,
        ctx,
        expression: Option(str, "f(x)", name="함수", required=True),
        x: Option(int, "미분계수를 구할 경우만 입력", name="x", default=None),
    ):
        try:
            f_x = expression
            expression = utils.math.Expression(expression)
            if expression.terms[0].degree > 10:
                if x is not None:
                    embed = discord.Embed(
                        title="⚠️ 명령어 사용 제한",
                        description="10차 방정식 이상은 미분계수 계산이 제한되었습니다",
                        color=warncolor,
                    )
                    await ctx.respond(embed=embed)
                    return
            if len(expression.terms) > 20:
                embed = discord.Embed(
                    title="⚠️ 명령어 사용 제한",
                    description="항은 20개 이상 입력 불가합니다",
                    color=warncolor,
                )
                await ctx.respond(embed=embed)
                return
            f_prime_x = []
            for i in expression.terms:
                temp = i
                if temp.degree == 0:
                    continue
                temp.coefficient *= temp.degree
                temp.degree -= 1
                f_prime_x.append(temp)
            f_prime_x = utils.math.Expression.from_terms(f_prime_x)
            embed = discord.Embed(title="미분 결과", color=embedcolor)
            embed.add_field(name="f(x)", value=f_x, inline=False)
            embed.add_field(
                name="f`(x)",
                value=str(f_prime_x),
                inline=False,
            )
            if x is not None:
                result = f_prime_x.substitute(x)
                embed.add_field(name=f"f`({x})", value=str(result), inline=False)
            await ctx.respond(embed=embed)
        except Exception as e:
            raise errors.WrongExpression

    @commands.slash_command(name="적분", description="미지수가 1개인 f(x)를 적분")
    @commands.max_concurrency(3)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def integral(
        self,
        ctx,
        expression: Option(str, "f(x)", name="함수", required=True),
        section: Option(str, "정적분 구간을 /로 구분해 입력", name="구간", default=None),
    ):
        try:
            if section is not None:
                splitted = section.split("/")
                a = int(splitted[0])
                b = int(splitted[1])
            f_x = expression
            expression = utils.math.Expression(expression)
            if expression.terms[0].degree > 10:
                if section is not None:
                    embed = discord.Embed(
                        title="⚠️ 명령어 사용 제한",
                        description="10차 방정식 이상은 정적분 계산이 제한되었습니다",
                        color=warncolor,
                    )
                    await ctx.respond(embed=embed)
                    return
            if len(expression.terms) > 20:
                embed = discord.Embed(
                    title="⚠️ 명령어 사용 제한",
                    description="항은 20개 이상 입력 불가합니다",
                    color=warncolor,
                )
                await ctx.respond(embed=embed)
                return
            F_x = []
            for i in expression.terms:
                temp = i
                temp.degree += 1
                temp.coefficient /= temp.degree
                F_x.append(temp)
            F_x = utils.math.Expression.from_terms(F_x)
            embed = discord.Embed(title="적분 결과", color=embedcolor)
            embed.add_field(name="f(x)", value=f_x, inline=False)
            embed.add_field(
                name="F(x)",
                value=str(F_x) + " + C",
                inline=False,
            )
            if section is not None:
                result = F_x.substitute(b) - F_x.substitute(a) if a != b else 0
                embed.add_field(
                    name=f"F({b}) - F({a})", value=str(result), inline=False
                )
            await ctx.respond(embed=embed)
        except Exception as e:
            raise errors.WrongExpression

    fraction = SlashCommandGroup("분수", "분수 계산 관련 명령어들")

    @fraction.command(name="약분", description="분수 약분")
    @commands.max_concurrency(3)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def fraction_simplify(self, fraction: Option(str, "약분할 분수", name="분수")):
        try:
            s_fraction = utils.math.Fraction(fraction)
            embed = discord.Embed(title="약분 결과", color=embedcolor)
            embed.add_field(name="약분 전", value=fraction, inline=False)
            embed.add_field(name="약분 후", value=str(s_fraction), inline=False)
            await ctx.respond(embed=embed)
        except:
            raise errors.WrongExpression

    @fraction.command(name="연산", description="분수 사칙연산")
    @commands.max_concurrency(3)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def fraction_calculate(
        self,
        frac1: Option(str, "첫번째 분수", name="분수1", required=True),
        operator: Option(str, "연산자", choices=["+", "-", "/", "*"]),
        frac2: Option(str, "두번째 분수", name="분수2", required=True),
    ):
        try:
            frac1 = utils.math.Fraction(frac1)
            frac2 = utils.math.Fraction(frac2)
            expression = f"{frac1} {operator} {frac2}"
            result = eval(expression)
            embed = discord.Embed(
                title="연산 결과", description=f"{expression} = {result}", color=embedcolor
            )
            await ctx.respond(embed=embed)
        except:
            raise errors.WrongExpression


def setup(bot):
    bot.add_cog(Math(bot))
