import discord
from discord import app_commands, Activity, ActivityType
import asyncio

TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
client.tree = app_commands.CommandTree(client)

# 🟢 رومات بدون رياكشن
enabled_channels = set()

# 🟢 رومات مع رياكشن
reaction_channels = set()

current_line = None
GUILD_ID = 935959922317860934


# 🟢 تحديث الحالة
async def update_status():
    await client.wait_until_ready()

    while not client.is_closed():
        guild = client.get_guild(GUILD_ID)

        if guild:
            members = guild.member_count

            await client.change_presence(
                activity=Activity(
                    type=ActivityType.playing,
                    name=f"Cloud Services | {members} members now"
                )
            )

        await asyncio.sleep(10)


@client.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)

    client.tree.copy_global_to(guild=guild)
    await client.tree.sync(guild=guild)

    print(f"Logged in as {client.user}")

    client.loop.create_task(update_status())


# 🟢 روم بدون رياكشن
@client.tree.command(name="setchannel", description="تفعيل الخط بدون رياكشن")
async def setchannel(interaction: discord.Interaction):
    enabled_channels.add(interaction.channel.id)
    reaction_channels.discard(interaction.channel.id)
    await interaction.response.send_message("✅ تم تفعيل الخط بدون رياكشن")


# 🟢 روم مع رياكشن
@client.tree.command(name="setchannel_reaction", description="تفعيل الخط مع رياكشن")
async def setchannel_reaction(interaction: discord.Interaction):
    reaction_channels.add(interaction.channel.id)
    enabled_channels.discard(interaction.channel.id)
    await interaction.response.send_message("💖 تم تفعيل الخط مع رياكشن")


# 🟢 إيقاف الروم
@client.tree.command(name="removechannel", description="إيقاف الخط في هذا الروم")
async def removechannel(interaction: discord.Interaction):
    enabled_channels.discard(interaction.channel.id)
    reaction_channels.discard(interaction.channel.id)
    await interaction.response.send_message("❌ تم إيقاف الخط")


# 🟢 إضافة خط
@client.tree.command(name="addline", description="إضافة خط")
@app_commands.describe(text="النص")
async def addline(interaction: discord.Interaction, text: str):
    global current_line
    current_line = text
    await interaction.response.send_message("✅ تم حفظ الخط")


# 🟢 حذف خط
@client.tree.command(name="reline", description="حذف الخط")
async def reline(interaction: discord.Interaction):
    global current_line
    current_line = None
    await interaction.response.send_message("♻️ تم حذف الخط")


# 🟢 عرض الخط
@client.tree.command(name="line", description="عرض الخط")
async def line(interaction: discord.Interaction):
    if not current_line:
        await interaction.response.send_message("❌ ما فيه خط")
        return

    await interaction.response.send_message(current_line)


# 🟢 الأحداث
@client.event
async def on_message(message):
    if message.author.bot:
        return

    # 🟢 أمر خط للأدمن
    if message.content == "خط":
        if message.author.guild_permissions.administrator:
            if current_line:
                await message.channel.send(current_line)
            else:
                await message.channel.send("❌ ما فيه خط محفوظ")
        else:
            await message.channel.send("🚫 ما عندك صلاحية")
        return

    # 🟢 بدون رياكشن
    if message.channel.id in enabled_channels:
        if current_line:
            await message.channel.send(current_line)

    # 🟢 مع رياكشن
    if message.channel.id in reaction_channels:

        try:
            await message.add_reaction("<a:Cloude_Rose:1495925679219277864>")
        except:
            pass

        if current_line:
            await message.channel.send(current_line)


client.run(TOKEN)