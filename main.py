@bot.command(name='Uun')
@commands.has_permissions(administrator=True)
async def uun_setup(ctx):
    # المنشن خارج الإمبيد للتنبيه
    content = "@everyone @here"
    
    # العبارة المطورة (ليست نسخ لصق)
    description = (
        "**Unleash your potential and manifest your dreams with Uun.**\n"
        "*Elevate your spirit and join our elite community.*\n\n"
        "**React with 〰️ to unlock the server channels.**"
    )
    
    embed = discord.Embed(
        title="✨ Welcome to the World of Uun",
        description=description, 
        color=0xf3c1cf # اللون الوردي الفخم
    )
    
    # إضافة صورة البنر 
    embed.set_image(url="https://googleusercontent.com/image_generation_content/17")
    
    # إضافة تذييل (Footer) لإضفاء لمسة احترافية
    embed.set_footer(text="Uun Community • Excellence & Spirit")
    
    # إرسال الرسالة
    message = await ctx.send(content=content, embed=embed)
    
    # إضافة الرياكشن التلقائي
    await message.add_reaction(VERIFY_EMOJI)
    
    # حذف رسالة الأمر
    await ctx.message.delete()
