import discord
from discord.ext import commands
import utils
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
        embed = discord.Embed(title="오류", description=str(error), color=errorcolor)
        embed.add_field(name="실행 유저", value=f"{ctx.author} ({ctx.author.id})")
        embed.add_field(name="실행 장소", value=f"{ctx.channel.mention}\n{ctx.guild.name}")
        message = await self.bot.get_channel(
            config.BOT.test_log_channel
            if config.BOT.debug_mode
            else config.BOT.log_channel
        ).send(embed=embed)
        if not isinstance(error, utils.ReportError):
            embed = discord.Embed(
                title="❌ 명령어 실행 불가",
                description="예기치 않은 문제로 인해 명령어 실행이 불가능합니다.\n아래 ID와 스크린샷, 사용한 명령어 등을 캡처해 보내주시면 오류 해결에 큰 도움이 됩니다.",
                color=errorcolor,
            )
            embed.add_field(name="에러 ID", value=str(message.id))
            await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Listener(bot))
