import discord
from discord.ext import commands
import os

# إعداد البوت والـ Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# إعدادات رتب التحقق والألوان
VERIFY_ROLE_NAME = "Uun"
VERIFY_EMOJI = "〰️"

# --- كلاس القائمة المنسدلة للألوان ---
class ColorSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="White", description="Change your name color to White", emoji="⚪", value="w"),
            discord.SelectOption(label="Red", description="Change your name color to Red", emoji="🔴", value="r"),
            discord.SelectOption(label="Green", description="Change your name color to Green", emoji="🟢", value="g"),
            discord.SelectOption(label="Purple", description="Change your name color to Purple", emoji="🟣", value="p"),
        ]
        super().__init__(placeholder="Choose your favorite color...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        selected_role_name = self.values[0]
        role = discord.utils.get(guild.roles, name=selected_role_name)
        
        if not role:
            await interaction.response.send_message(f"Role '{selected_role_name}' not found in server settings!", ephemeral=True)
            return

        # قائمة بكل رتب الألوان الممكنة لمسح القديم منها
        all_color_names = ["w", "r", "g", "p"]
        roles_to_remove = [discord.utils.get(guild.roles, name=n) for n in all_color_names]
        roles_to_remove = [r for r in roles_to_remove if r and r in interaction.user.roles]
        
        try:
            if roles_to_remove:
                await interaction.user.remove_roles(*roles_to_remove)
            
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ Your color has been updated to: **{role.name.upper()}**", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to manage your roles. Check my role position!", ephemeral=True)

class ColorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ColorSelect())

# --- الأوامر ---

@bot.command(name='Uun')
@commands.has_permissions(administrator=True)
async def uun_setup(ctx):
    content = "@everyone @here"
    description = (
        "**Unleash your potential and manifest your dreams with Uun.**\n"
        "*Elevate your spirit and join our elite community.*\n\n"
        "**React with 〰️ to unlock the server channels.**"
    )
    embed = discord.Embed(title="✨ Welcome to Uun", description=description, color=0xf3c1cf)
    embed.set_image(url="https://googleusercontent.com/image_generation_content/17")
    message = await ctx.send(content=content, embed=embed)
    await message.add_reaction(VERIFY_EMOJI)
    await ctx.message.delete()

@bot.command(name='color')
@commands.has_permissions(administrator=True)
async def color_setup(ctx):
    embed = discord.Embed(
        title="🎨 Pick Your Identity Color",
        description=(
            "Click the menu below to select your unique name color.\n"
            "**Note:** Selecting a new color will replace your current one."
        ),
        color=0x2b2d31
    )
    embed.set_footer(text="Uun Community • Color System")
    await ctx.send(embed=embed, view=ColorView())
    await ctx.message.delete()

# نظام الرياكشن للتحقق (Uun)
@bot.event
async def on_raw_reaction_add(payload):
    if payload.member.bot: return
    if str(payload.emoji) == VERIFY_EMOJI:
        guild = bot.get_guild(payload.guild_id)
        role = discord.utils.get(guild.roles, name=VERIFY_ROLE_NAME)
        if role:
            try: await payload.member.add_roles(role)
            except: pass

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} | Systems Active")

bot.run(os.getenv('DISCORD_TOKEN'))
