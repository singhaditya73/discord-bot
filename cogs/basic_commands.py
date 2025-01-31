import discord
from discord.ext import commands

class BasicCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Simple ping command to check bot responsiveness."""
        await ctx.send(f"🏓 Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command(name='help')
    async def help_command(self, ctx):
        """Display help commands for the bot."""
        embed = discord.Embed(title="Help Commands", description="Here are some commands you can use with the bot:", color=discord.Color.blue())
        embed.add_field(name="!ping", value="Check the bot's response time.", inline=False)
        embed.add_field(name="!startcomp", value="Start a new competition in the channel.", inline=False)
        embed.add_field(name="!answer", value="Submit your answer to the current question in DM.", inline=False)
        embed.add_field(name="!lb", value="Display the current competition leaderboard.", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(BasicCommand(bot))
