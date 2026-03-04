import discord
from discord.ext import commands
import os

# إعداد البوت والـ Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# إعدادات رتب التحقق والالوان
VERIFY_ROLE_NAME = "Uun"
VERIFY_EMOJI = "〰️"
COLOR_ROLES = {
    "white_btn": "w",
    "red_btn": "r",
    "green_btn": "g",
    "purple_btn": "p"
}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} | Systems Active")

# --- كلاس الأزرار للألوان ---
class ColorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # الأزرار تبقى شابة دائماً

    async def handle_color(self, interaction: discord.Interaction, role_name: str):
        guild = interaction.guild
        role = discord.utils.get(guild.roles, name=role_name)
        
        if not role:
            await interaction.response.send_message(f"Role '{role_name}' not found!", ephemeral=True)
            return

        # سحب الألوان القديمة (عشان يختار لون واحد بس)
        roles_to_remove = [discord.utils.get(guild.roles, name=r) for r in COLOR_ROLES.values()]
        roles_to_remove = [r for r in roles_to_remove if r in interaction.user.roles]
        
        await interaction.user.remove_roles(*roles_to_remove)
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"✅ Your color has been updated to: **{role_name.upper()}**", ephemeral=True)

    @discord.ui.button(label="White", style=discord.ButtonStyle.secondary, custom_id="white_btn")
    async def white_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_color(interaction, "w")

    @discord.ui.button(label="Red", style=discord.ButtonStyle.danger, custom_id="red_btn")
    async def red_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_color(interaction, "r")

    @discord.ui.button(label="Green", style=discord.ButtonStyle.success, custom_id="green_btn")
    async def green_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_color(interaction, "g")

    @discord.ui.button(label="Purple", style=discord.ButtonStyle.primary, custom_id="purple_btn")
    async def purple_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_color(interaction, "p")

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
        title="🎨 Identity Colors",
        description=(
            "Personalize your profile by choosing your name color below.\n"
            "*Note: You can only have one active color at a time.*"
        ),
        color=0x2b2d31 # لون غامق فخم
    )
    embed.set_footer(text="Uun Community • Color System")
    await ctx.send(embed=embed, view=ColorView())
    await ctx.message.delete()

# نظام الرياكشن للتحقق
@bot.event
async def on_raw_reaction_add(payload):
    if payload.member.bot: return
    if str(payload.emoji) == VERIFY_EMOJI:
        guild = bot.get_guild(payload.guild_id)
        role = discord.utils.get(guild.roles, name=VERIFY_ROLE_NAME)
        if role:
            try: await payload.member.add_roles(role)
            except: pass

bot.run(os.getenv('DISCORD_TOKEN'))
