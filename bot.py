import discord
from discord import app_commands, Activity, ActivityType
import asyncio
import os

TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True  # مهم للصوت

client = discord.Client(intents=intents)
client.tree = app_commands.CommandTree(client)

# 🟢 الرومات
enabled_channels = set()
reaction_channels = set()

GUILD_ID = 935959922317860934

# 🟢 روم الصوت
VOICE_CHANNEL_ID = 1496124315270254703

# 🟢 صورة الخط (بدون Embed)
IMAGE_URL = "https://cdn.discordapp.com/attachments/1495165123789062324/1495898310765056072/Picsart_26-04-19_17-16-50-332.jpg"

# 🟢 منع التكرار الحقيقي
processed_messages = set()


# 🟢 اتصال الصوت دائم
async def keep_voice_connected():
    await client.wait_until_ready()

    while not client.is_closed():
        guild = client.get_guild(GUILD_ID)

        if guild:
            channel = guild.get_channel(VOICE_CHANNEL_ID)
            voice_client = discord.utils.get(client.voice_clients, guild=guild)

            if not voice_client or not voice_client.is_connected():
                try:
                    await channel.connect()
                except:
                    pass

        await asyncio.sleep(5)


# 🟢 الحالة
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
    client.loop.create_task(keep_voice_connected())  # تشغيل نظام الصوت


# 🟢 أوامر التفعيل
@client.tree.command(name="setchannel", description="تفعيل بدون رياكشن")
async def setchannel(interaction: discord.Interaction):
    enabled_channels.add(interaction.channel.id)
    reaction_channels.discard(interaction.channel.id)
    await interaction.response.send_message("✅ تم التفعيل بدون رياكشن")


@client.tree.command(name="setchannel_reaction", description="تفعيل مع رياكشن")
async def setchannel_reaction(interaction: discord.Interaction):
    reaction_channels.add(interaction.channel.id)
    enabled_channels.discard(interaction.channel.id)
    await interaction.response.send_message("💖 تم التفعيل مع رياكشن")


@client.tree.command(name="removechannel", description="إيقاف")
async def removechannel(interaction: discord.Interaction):
    enabled_channels.discard(interaction.channel.id)
    reaction_channels.discard(interaction.channel.id)
    await interaction.response.send_message("❌ تم الإيقاف")


# 🟢 إرسال الخط
async def send_line(channel):
    await channel.send(IMAGE_URL)


# 🟢 on_message
@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.id in processed_messages:
        return

    processed_messages.add(message.id)

    if message.content == "خط":
        if message.author.guild_permissions.administrator:
            await send_line(message.channel)
        else:
            await message.channel.send("🚫 ما عندك صلاحية")
        return

    if message.channel.id in enabled_channels:
        await send_line(message.channel)
        return

    if message.channel.id in reaction_channels:
        try:
            await message.add_reaction("<a:Cloude_Rose:1495925679219277864>")
        except:
            pass

        await send_line(message.channel)
        return


client.run(TOKEN)