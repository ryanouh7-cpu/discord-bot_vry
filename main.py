import discord
from discord.ext import commands
import os

# 1. تعريف البوت والـ Intents (هذا الجزء اللي كان ناقص)
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

VERIFY_ROLE_NAME = "Uun"
VERIFY_EMOJI = "〰️"

@bot.event
async def on_ready():
    print(f"Security Bot Active | Name: {bot.user.name}")

# 2. أمر !Uun بالعبارة المطورة
@bot.command(name='Uun')
@commands.has_permissions(administrator=True)
async def uun_setup(ctx):
    content = "@everyone @here"
    
    # العبارة المطورة وغير المنسوخة
    description = (
        "**Unleash your potential and manifest your dreams with Uun.**\n"
        "*Elevate your spirit and join our elite community.*\n\n"
        "**React with 〰️ to unlock the server channels.**"
    )
    
    embed = discord.Embed(
        title="✨ Welcome to the World of Uun",
        description=description, 
        color=0xf3c1cf
    )
    
    # رابط البنر اللي سويناه لك
    embed.set_image(url="https://googleusercontent.com/image_generation_content/17")
    embed.set_footer(text="Uun Community • Excellence & Spirit")
    
    message = await ctx.send(content=content, embed=embed)
    await message.add_reaction(VERIFY_EMOJI)
    await ctx.message.delete()

# 3. نظام الرياكشن لإعطاء الرتبة
@bot.event
async def on_raw_reaction_add(payload):
    if payload.member.bot: return
    if str(payload.emoji) == VERIFY_EMOJI:
        guild = bot.get_guild(payload.guild_id)
        role = discord.utils.get(guild.roles, name=VERIFY_ROLE_NAME)
        if role:
            try:
                await payload.member.add_roles(role)
            except:
                print("Missing Permissions!")

# 4. تشغيل البوت (تأكد أن المتغير في ريلوي بنفس الاسم)
bot.run(os.getenv('DISCORD_TOKEN'))
