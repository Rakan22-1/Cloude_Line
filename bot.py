import discord
from discord import app_commands, Activity, ActivityType
import asyncio
import os
import json

TOKEN = os.environ.get("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

client = discord.Client(intents=intents)
client.tree = app_commands.CommandTree(client)

# 🧠 بيانات القنوات (تتحفظ بعد الريستارت)
DATA_FILE = "channels.json"
enabled_channels = set()
reaction_channels = set()

# 🟢 إعدادات
GUILD_ID = 935959922317860934
VOICE_CHANNEL_ID = 1496124315270254703

IMAGE_URL = "https://cdn.discordapp.com/attachments/1495165123789062324/1495898310765056072/Picsart_26-04-19_17-16-50-332.jpg"

processed_messages = set()


# 💾 حفظ + تحميل البيانات
def load_data():
    global enabled_channels, reaction_channels
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            enabled_channels = set(data.get("enabled", []))
            reaction_channels = set(data.get("reaction", []))
    except:
        enabled_channels = set()
        reaction_channels = set()


def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({
            "enabled": list(enabled_channels),
            "reaction": list(reaction_channels)
        }, f)


# 🎧 الصوت
async def keep_voice_connected():
    await client.wait_until_ready()
    print("🎧 Voice system started")

    while True:
        try:
            guild = client.get_guild(GUILD_ID)
            if not guild:
                await asyncio.sleep(5)
                continue

            channel = guild.get_channel(VOICE_CHANNEL_ID)
            if not channel:
                await asyncio.sleep(5)
                continue

            voice = guild.voice_client

            if voice and voice.is_connected():
                await asyncio.sleep(10)
                continue

            try:
                print("🔌 Connecting to voice...")
                await channel.connect(self_deaf=True, self_mute=True, timeout=10)
                print("✅ Voice connected")

            except Exception as e:
                print("❌ Voice error:", e)
                await asyncio.sleep(15)

        except Exception as e:
            print("Loop error:", e)

        await asyncio.sleep(15)


# 📊 الحالة
async def update_status():
    await client.wait_until_ready()

    while True:
        guild = client.get_guild(GUILD_ID)

        if guild:
            await client.change_presence(
                activity=Activity(
                    type=ActivityType.playing,
                    name=f"Cloud Services | {guild.member_count} members"
                )
            )

        await asyncio.sleep(10)


# 🚀 تشغيل
@client.event
async def on_ready():
    load_data()
    print(f"Logged in as {client.user}")
    print("STARTING BOT...")

    asyncio.create_task(keep_voice_connected())
    asyncio.create_task(update_status())


# 🧾 إرسال الخط
async def send_line(channel):
    try:
        await channel.send(IMAGE_URL)
    except Exception as e:
        print("Send error:", e)


# 💬 الرسائل
@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.id in processed_messages:
        return

    processed_messages.add(message.id)

    if message.content == "خط":
        await send_line(message.channel)


# 🟢 أوامر السلاش
@client.tree.command(name="setchannel")
async def setchannel(interaction: discord.Interaction):
    enabled_channels.add(interaction.channel.id)
    save_data()
    await interaction.response.send_message("✅ تم التفعيل بدون رياكشن")


@client.tree.command(name="setchannel_reaction")
async def setchannel_reaction(interaction: discord.Interaction):
    reaction_channels.add(interaction.channel.id)
    save_data()
    await interaction.response.send_message("💖 تم التفعيل مع رياكشن")


@client.tree.command(name="removechannel")
async def removechannel(interaction: discord.Interaction):
    enabled_channels.discard(interaction.channel.id)
    reaction_channels.discard(interaction.channel.id)
    save_data()
    await interaction.response.send_message("❌ تم الإيقاف")


# 🔥 تشغيل البوت
client.run(TOKEN)