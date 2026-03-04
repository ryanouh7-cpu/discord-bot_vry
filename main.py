import discord
from discord.ext import commands
import os

# إعداد البوت والـ Intents
intents = discord.Intents.default()
intents.members = True  # ضروري لإعطاء الرتب للأعضاء
intents.message_content = True # ضروري لقراءة الأوامر

bot = commands.Bot(command_prefix='!', intents=intents)

# إعدادات الرتبة والرياكشن
VERIFY_ROLE_NAME = "Uun"
VERIFY_EMOJI = "〰️"

@bot.event
async def on_ready():
    print(f"Security Bot Active | Name: {bot.user.name}")

# الأمر الجديد !Uun
@bot.command(name='Uun')
@commands.has_permissions(administrator=True)
async def uun_setup(ctx):
    # المنشن خارج الإمبيد لضمان وصول التنبيه
    content = "@everyone @here"
    
    # النص المقتبس من الصورة
    description = (
        "Achieve all your dreams with Uun.\n"
        "Nurture your spirit"
    )
    
    embed = discord.Embed(
        description=description, 
        color=0xf3c1cf # اللون الوردي المعتمد
    )
    
    # إضافة صورة البنر الفخمة (رابط الصورة التي صممناها)
    embed.set_image(url="https://googleusercontent.com/image_generation_content/17")
    
    # إرسال الرسالة
    message = await ctx.send(content=content, embed=embed)
    
    # إضافة الرياكشن التلقائي
    await message.add_reaction(VERIFY_EMOJI)
    
    # حذف رسالة الأمر لتنظيف الشات
    await ctx.message.delete()

@bot.event
async def on_raw_reaction_add(payload):
    """إعطاء الرتبة تلقائياً عند الضغط على الرياكشن"""
    if payload.member.bot: return
    
    if str(payload.emoji) == VERIFY_EMOJI:
        guild = bot.get_guild(payload.guild_id)
        role = discord.utils.get(guild.roles, name=VERIFY_ROLE_NAME)
        
        if role:
            try:
                await payload.member.add_roles(role)
                print(f"Done: Added role to {payload.member.name}")
            except discord.Forbidden:
                print("Error: Check Bot Role Position!")

# تشغيل البوت باستخدام التوكن من Railway
bot.run(os.getenv('DISCORD_TOKEN'))
