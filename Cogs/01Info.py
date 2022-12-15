import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
import config
from datetime import timedelta, datetime

embedcolor = config.BOT.embedcolor
errorcolor = config.BOT.errorcolor
warncolor = config.BOT.warncolor


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    info = SlashCommandGroup("정보", "유저/서버/ThinkingBot 등 정보 조회")

    @info.command(name="유저", description="유저 정보 조회")
    async def info_user(self, ctx, user: discord.User = None):
        user = ctx.guild.get_member((user or ctx.author).id)
        embed = discord.Embed(
            title=f'{"🤖" if user.bot else "👤"} {user} 정보', color=embedcolor
        )
        embed.set_thumbnail(url=(user.guild_avatar or user.default_avatar).url)
        if user.banner is not None:
            embed.set_image(url=user.banner.url)
        embed.add_field(name="서버 닉네임", value=user.display_name, inline=False)
        embed.add_field(name="ID", value=str(user.id), inline=False)
        embed.add_field(
            name="계정 생성일",
            value=user.created_at.strftime("%Y/%m/%d %H:%M:%S"),
            inline=False,
        )
        embed.add_field(
            name="서버 가입일",
            value=user.joined_at.strftime("%Y/%m/%d %H:%M:%S"),
            inline=False,
        )
        if user.timed_out:
            embed.add_field(
                name="타임아웃 해제",
                value=user.communication_disabled_until.strftime("%Y/%m/%d %H:%M:%S"),
                inline=False,
            )
        roles = ", ".join([i.mention for i in user.roles[1:]])
        embed.add_field(
            name="역할 목록", value=roles if roles != "" else "없음", inline=False
        )
        await ctx.respond(embed=embed)

    @info.command(name="서버", description="서버 정보 조회")
    async def info_guild(self, ctx):
        embed = discord.Embed(
            title=f"{ctx.guild.name} 서버 정보",
            description=ctx.guild.description,
            color=embedcolor,
        )
        if ctx.guild.icon is not None:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        if ctx.guild.banner is not None:
            embed.set_image(url=ctx.guild.banner.url)
        embed.add_field(name="ID", value=str(ctx.guild.id), inline=False)
        embed.add_field(
            name="생성일자",
            value=ctx.guild.created_at.strftime("%Y/%m/%d %H:%M:%S"),
            inline=False,
        )
        embed.add_field(name="주인", value=ctx.guild.owner.mention, inline=False)
        embed.add_field(name="인원", value=str(ctx.guild.member_count), inline=False)
        if ctx.guild.rules_channel is not None:
            embed.add_field(
                name="규칙 채널", value=ctx.guild.rules_channel.mention, inline=False
            )
        embed.add_field(name="부스트 레벨", value=str(ctx.guild.premium_tier), inline=False)
        roles = ", ".join([i.mention for i in ctx.guild.roles[1:]])
        embed.add_field(
            name="역할 목록", value=roles if roles != "" else "없음", inline=False
        )
        await ctx.respond(embed=embed)

    @info.command(name="봇", description="ThinkingBot 정보 조회")
    async def info_thinkingbot(self, ctx):
        embed = discord.Embed(
            title="ThinkingBot 정보",
            description=f"[지원]({config.BOT.support_link})",
            color=embedcolor,
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(
            name="생성일",
            value=f'{self.bot.user.created_at.strftime("%Y/%m/%d")} (<t:{round(self.bot.user.created_at.timestamp())}:R>)',
            inline=False,
        )
        embed.add_field(name="제작자", value="<@1015942852582326292>", inline=False)
        embed.add_field(name="서버수", value=f"{len(self.bot.guilds)}", inline=False)
        embed.add_field(name="핑", value="측정중", inline=False)
        before = datetime.now()
        inter = await ctx.respond(embed=embed)
        after = datetime.now()
        embed.remove_field(len(embed.fields) - 1)
        ping = after - before
        embed.add_field(
            name="핑",
            value=f"{round(ping.seconds * 1000 + ping.microseconds / 1000)}ms",
            inline=False,
        )
        await inter.edit_original_response(embed=embed)


def setup(bot):
    bot.add_cog(Core(bot))
