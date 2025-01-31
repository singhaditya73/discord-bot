import discord
from discord.ext import commands
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.key = self.generate_key("your-secure-password")
        self.cipher_suite = Fernet(self.key)

    def generate_key(self, password):
        salt = b'salt_123'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    @commands.command()
    async def encrypt(self, ctx, *, message: str):
        try:
            encrypted_message = self.cipher_suite.encrypt(message.encode())
            encoded_message = base64.b64encode(encrypted_message).decode()
            await ctx.send(f"Encrypted message: ```{encoded_message}```")
            if not isinstance(ctx.channel, discord.DMChannel):
                await ctx.message.delete()
        except Exception as e:
            await ctx.send(f"Error encrypting message: {str(e)}")

    @commands.command()
    async def decrypt(self, ctx, *, encrypted_message: str):
        try:
            decoded_message = base64.b64decode(encrypted_message.encode())
            decrypted_message = self.cipher_suite.decrypt(decoded_message)
            await ctx.author.send(f"Decrypted message: ```{decrypted_message.decode()}```")
            if not isinstance(ctx.channel, discord.DMChannel):
                await ctx.message.delete()
        except Exception as e:
            await ctx.send(f"Error decrypting message: {str(e)}")

async def setup(bot):
    await bot.add_cog(Crypto(bot))
