import discord
from discord.ext import commands
import utils.errors as errors
import config

warncolor = config.BOT.warncolor
errorcolor = config.BOT.errorcolor


class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        text = f'Ready\t: {"Test" if config.BOT.debug_mode else "Official"} Bot'
        print(text)
        await self.bot.get_channel(
            config.BOT.test_log_channel
            if config.BOT.debug_mode
            else config.BOT.log_channel
        ).send(text)

    @commands.Cog.listener()
    async def before_invoke(self, ctx):
        await ctx.interaction.response.defer()
        if ctx.command.cooldown is not None and ctx.author.id in config.BOT.owner_ids:
            ctx.command.cooldown.reset()

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        error = error.original
        if isinstance(error, discord.CheckFailure):
            return
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="⚠️ 명령어 사용 제한",
                description=f"현재 명령어는 {round(error.retry_after, 1)}초 후 다시 사용 가능합니다",
                color=warncolor,
            )
            await ctx.respond(embed=embed)
            return
        elif isinstance(error, errors.WrongExpression):
            embed = discord.Embed(title="수식 입력 방법", color=warncolor)
            embed.add_field(name="미지수 사용", value="> 미지수는 x 1개만 사용 가능합니다", inline=False)
            embed.add_field(
                name="거듭제곱 표현",
                value="> 거듭제곱은 ^ 뒤에 제곱할 숫자를 입력하셔야 합니다\n> 차수는 0 이상의 정수만 가능합니다",
                inline=False,
            )
            embed.add_field(
                name="분수인 계수 표현",
                value="> 분수는 `분모/분자`의 형태로 입력후 필히 괄호로 감싸주세요",
                inline=False,
            )
            await ctx.respond(embed=embed)
        elif isinstance(error, errors.FractionDenoZero):
            embed = discord.Embed(
                title="⚠️ 수식 오류", description="분모는 0이 될 수 없습니다.", color=warncolor
            )
            await ctx.respond(embed=embed)
        embed = discord.Embed(title="오류", description=str(error), color=errorcolor)
        embed.add_field(name="실행 유저", value=f"{ctx.author} ({ctx.author.id})")
        embed.add_field(name="실행 장소", value=f"{ctx.channel.mention}\n{ctx.guild.name}")
        message = await self.bot.get_channel(
            config.BOT.test_log_channel
            if config.BOT.debug_mode
            else config.BOT.log_channel
        ).send(embed=embed)
        if not isinstance(error, errors.ReportError):
            embed = discord.Embed(
                title="❌ 명령어 실행 불가",
                description="예기치 않은 문제로 인해 명령어 실행이 불가능합니다.\n아래 ID와 스크린샷, 사용한 명령어 등을 캡처해 보내주시면 오류 해결에 큰 도움이 됩니다.",
                color=errorcolor,
            )
            embed.add_field(name="에러 ID", value=str(message.id))
            await ctx.respond(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        embed = discord.Embed(title="서버 참여", color=embedcolor)
        embed.add_field(name="서버 정보", value=f"{guild.name} ({guild.id})")
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(icon_url=guild.owner.avatar_url, text=f"{guild.owner}")
        await (self.bot.get_channel(config.BOT.log_channel)).send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        embed = discord.Embed(title="서버 퇴장", color=embedcolor)
        embed.add_field(name="서버 정보", value=f"{guild.name} ({guild.id})")
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(icon_url=guild.owner.avatar_url, text=f"{guild.owner}")
        await (self.bot.get_channel(config.BOT.log_channel)).send(embed=embed)


def setup(bot):
    bot.add_cog(Listener(bot))
