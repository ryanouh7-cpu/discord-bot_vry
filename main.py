import discord
from discord.ext import commands
import os

# إعداد البوت والـ Intents
intents = discord.Intents.default()
intents.members = True  # ضروري لإعطاء الرتب
intents.message_content = True 

bot = commands.Bot(command_prefix='!', intents=intents)

VERIFY_ROLE_NAME = "Uun"
VERIFY_EMOJI = "〰️"

@bot.event
async def on_ready():
    print(f"Security Bot Active | Name: {bot.user.name}")

@bot.command(name='setup')
@commands.has_permissions(administrator=True)
async def setup(ctx):
    content = "@everyone @here"
    description = (
        "Achieve all your dreams with Uun.\n"
        "Nurture your spirit"
    )
    
    embed = discord.Embed(description=description, color=0xf3c1cf)
    # إذا تبي صورة البنر تظهر، فك التعليق عن السطر تحت وحط الرابط
    # embed.set_image(url="رابط_صورة_البنر")
    
    message = await ctx.send(content=content, embed=embed)
    await message.add_reaction(VERIFY_EMOJI)
    await ctx.message.delete()

@bot.event
async def on_raw_reaction_add(payload):
    if payload.member.bot: return
    if str(payload.emoji) == VERIFY_EMOJI:
        guild = bot.get_guild(payload.guild_id)
        role = discord.utils.get(guild.roles, name=VERIFY_ROLE_NAME)
        if role:
            try:
                await payload.member.add_roles(role)
            except discord.Forbidden:
                print("Missing Permissions to add role!")

bot.run(os.getenv('DISCORD_TOKEN'))
