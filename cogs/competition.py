import discord
from discord.ext import commands
import datetime
import asyncio
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Competition(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_competitions = {}
        self.leaderboard = defaultdict(int)
        self.question_timestamps = {}
        self.participant_channels = defaultdict(list)  # To store multiple participants for each channel
        self.config = {
            'total_questions': 10,
            'points_per_question': 100,
            'point_loss_per_minute': 10,
            'question_timeout': 30  # Seconds
        }
        self.questions = [
    {
        "question": "The lush, verdant meadow stretched out before them, a tapestry of vibrant greens and colorful wildflowers.  A gentle stream meandered through the landscape, its soothing murmurs a symphony to their ears. As they walked, they noticed a peculiar pattern in the placement of the rocks along the riverbank - was it merely a coincidence, or was there a hidden message waiting to be uncovered? Determined to unravel the mystery, they scanned the area, their eyes darting from one detail to the next. Little did they know that the key to unlocking the secrets of this enchanting place lay in the most unexpected of places.\n Question: What is the hidden phrase that can be extracted from the first letter of each sentence in the paragraph?", 
        "answer": "meadow"
    },
    {
        "question": "What is the minimum number of emojis needed to represent a secure password in this game?\n hint: answer should be emoji only", 
        "answer": "🔒"
    },
    {
        "question": "A password policy requires a password to be 8 characters long, consisting of uppercase letters (26), lowercase letters (26), and digits (10). How many possible passwords can be created?\n hint: answer should be in format : x^n", 
        "answer": "62^8"
    },
    {
        "question": "What is the term for an attack where a hacker exploits a web application's database query vulnerabilities?", 
        "answer": "sql injection"
    },
    {
        "question": "Story: Alice discovered that her password had been stolen after noticing some missing files on her laptop. The day before, she had left her laptop unlocked to take a call while Bob, Carol, and Dave were around. Bob had asked Alice for help with a technical issue, Carol was in the break room talking to others, and Dave had been working late and kept to himself. \n Question: Who do you suspect stole Alice’s password?", 
        "answer": "dave"
    },
    {
        "question": "During your investigation, you find a SHA-1 hashed password in a suspicious log file. The hash is: b2e98ad6f6eb8508dd6a14cfa704bad7f05f6fb1 \n Your mission is to crack this hash to uncover the original password and proceed with the investigation.", 
        "answer": "qwerty"
    },
    {
        "question": "The password you need to unlock the next level of the investigation is hidden behind a series of clues. Use the following hints to guess the correct password: The password is 8 characters long. It includes at least one number. It has no special characters (only letters and numbers).The password starts with a letter.Guess the password that fits all of these criteria.", 
        "answer": "s3curity"
    },
    {
        "question": "What is the term for malicious software that infects the firmware of a system, making it persistent even after reboots and operating system reinstallation?", 
        "answer": "rootkit"
    },
    {
        "question": "A password policy requires a password of 4 characters, using only digits (0-9). How many possible passwords exist? \n hint: answer should be a interger x", 
        "answer": "10000"
    },
    {
        "question": "A man is looking at a picture of someone. His friend asks, \"Who are you looking at?\" The man replies, \"Brothers and sisters, I have none. But the father of the person in the picture is my father’s son.\" Who is the person in the picture? Give the answer.", 
        "answer": "son"
    }
]


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel in self.active_competitions:
            if not message.content.lower().startswith(('!lb', '!help')):
                try:
                    await message.delete()
                    await message.channel.send(
                        f"{message.author.mention} Only `!lb` and `!help` commands are allowed here. Please send your answers in DM to the bot!",
                        delete_after=5)
                except discord.Forbidden:
                    pass

    @commands.command(name='join')
    async def join_competition(self, ctx):
        """Allows users to join an ongoing competition."""
        competition_channel = ctx.channel

        if competition_channel in self.active_competitions:
            if ctx.author.id not in self.participant_channels[competition_channel]:
                self.participant_channels[competition_channel].append(ctx.author.id)
                await ctx.send(f"🎉 {ctx.author.mention} has joined the competition!")
            else:
                await ctx.send(f"❌ {ctx.author.mention}, you are already participating.")
        else:
            await ctx.send("❌ There is no active competition in this channel to join.")

    @commands.command(name='answer')
    @commands.dm_only()
    async def submit_answer(self, ctx, question_number: int, *, answer: str):
        try:
            for competition_channel, participants in self.participant_channels.items():
                if ctx.author.id in participants:
                    comp = self.active_competitions.get(competition_channel)

                    if not comp or not comp['is_active']:
                        await ctx.send("❌ No active competition found!")
                        return

                    if not 1 <= question_number <= self.config['total_questions']:
                        await ctx.send(f"❌ Question number must be between 1 and {self.config['total_questions']}")
                        return

                    if question_number != comp['current_question']:
                        await ctx.send(f"❌ This is not the current question. Please answer question {comp['current_question']}.")
                        return

                    correct_answer = self.questions[question_number - 1]['answer'].lower()
                    if answer.lower().strip() != correct_answer:
                        await ctx.send("❌ Incorrect answer. Try again!")
                        return

                    time_taken = datetime.datetime.now() - self.question_timestamps[question_number]
                    minutes_taken = time_taken.total_seconds() / 60
                    points = self.config['points_per_question']
                    points_lost = min(int(minutes_taken) * self.config['point_loss_per_minute'], points)
                    final_points = max(0, points - points_lost)

                    self.leaderboard[ctx.author.name] += final_points

                    success_embed = discord.Embed(title="✅ Correct Answer!", color=discord.Color.green())
                    success_embed.add_field(name="Points Earned", value=str(final_points))
                    success_embed.add_field(name="Time Taken", value=f"{minutes_taken:.1f} minutes")
                    await ctx.send(embed=success_embed)

                    await competition_channel.send(f"🎉 {ctx.author.mention} answered correctly!")
                    await self.show_leaderboard(competition_channel)

                    comp['current_question'] += 1
                    await self.ask_next_question(competition_channel)

                    return

            await ctx.send("❌ You are not currently participating in any competition!")

        except Exception as e:
            logger.error(f"Error processing answer: {e}")
            await ctx.send("❌ An error occurred while processing your answer.")

    @commands.command(name='startcomp')
    async def start_competition(self, ctx, channel: discord.TextChannel = None):
        if not channel:
            channel = ctx.channel

        if channel in self.active_competitions:
            await ctx.send("❌ There is already an active competition in this channel.")
            return

        self.active_competitions[channel] = {
            'is_active': True,
            'current_question': 1,
            'total_questions': self.config['total_questions'],
            'points_per_question': self.config['points_per_question'],
            'point_loss_per_minute': self.config['point_loss_per_minute'],
            'question_timeout': self.config['question_timeout'],
            'questions': self.questions
        }

        await ctx.send(f"🎉 A new competition has started in {channel.mention}! Use `!join` to participate.")
        await self.ask_next_question(channel)

    async def ask_next_question(self, channel):
        if channel not in self.active_competitions:
            return

        comp = self.active_competitions[channel]
        current_question = comp['current_question']

        if current_question > self.config['total_questions']:
            await self.end_competition(channel)
            return

        question = self.questions[current_question - 1]['question']
        logger.info(f"Asking question {current_question}: {question}")
        embed = discord.Embed(title=f"❓ Question {current_question}", description=question, color=discord.Color.blue())
        embed.set_footer(text="Send your answer in DM to the bot using !answer")

        await channel.send(embed=embed)
        self.question_timestamps[current_question] = datetime.datetime.now()

        await asyncio.sleep(self.config['question_timeout'])

        if channel in self.active_competitions and comp['current_question'] == current_question:
            await channel.send(f"⏰ Time's up for question {current_question}! Moving to the next question.")
            comp['current_question'] += 1
            await self.ask_next_question(channel)

    @commands.command(name='lb')
    async def show_leaderboard(self, ctx):
        if ctx.channel in self.active_competitions:
            if self.leaderboard:
                await self.display_leaderboard(ctx.channel)
            else:
                await ctx.send("📊 No scores recorded for this competition!")
        else:
            await ctx.send("❌ There is no active competition to display a leaderboard for.")

    async def display_leaderboard(self, channel: discord.TextChannel):
        if self.leaderboard:
            embed = discord.Embed(title="🏆 Leaderboard", color=discord.Color.blue(), timestamp=datetime.datetime.now())
            for position, (name, score) in enumerate(sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True),
                                                     start=1):
                embed.add_field(name=f"{position}. {name}", value=f"Score: {score}", inline=False)
            await channel.send(embed=embed)
        else:
            await channel.send("📊 No scores recorded for this competition!")

    @commands.command(name='endcomp')
    async def end_competition_command(self, ctx, channel: discord.TextChannel = None):
        """Manually end the competition with the !endcomp command"""
        if not channel:
            channel = ctx.channel

        if channel in self.active_competitions:
            await self.end_competition(channel)
        else:
            await ctx.send("❌ There is no active competition in this channel to end.")

    async def end_competition(self, channel):
        if channel in self.active_competitions:
            del self.active_competitions[channel]
            await channel.send("🏁 The competition has ended!")
            await self.display_leaderboard(channel)

def setup(bot):
    bot.add_cog(Competition(bot))
