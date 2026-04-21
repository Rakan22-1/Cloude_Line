import discord
from discord import app_commands, Activity, ActivityType
import asyncio
import os

TOKEN = os.environ["TOKEN"]


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

client = discord.Client(intents=intents)
client.tree = app_commands.CommandTree(client)

# 🟢 الإعدادات
GUILD_ID = 935959922317860934
VOICE_CHANNEL_ID = 1496124315270254703

enabled_channels = set()
reaction_channels = set()
processed_messages = set()

IMAGE_URL = "https://cdn.discordapp.com/attachments/1495165123789062324/1495898310765056072/Picsart_26-04-19_17-16-50-332.jpg"


# 🎧 الصوت (نسخة ثابتة بدون انهيار)
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
                print("Voice channel not found")
                await asyncio.sleep(5)
                continue

            voice = guild.voice_client

            # إذا موجود داخل الروم خلاص لا يعيد اتصال
            if voice and voice.is_connected():
                await asyncio.sleep(10)
                continue

            try:
                print("🔌 Connecting to voice...")
                await channel.connect(
                    self_deaf=True,
                    self_mute=True,
                    timeout=10
                )
                print("✅ Voice connected")

            except Exception as e:
                print("❌ Voice connect error:", e)
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


# 🚀 تشغيل البوت
@client.event
async def on_ready():
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


# 💬 on_message
@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.id in processed_messages:
        return

    processed_messages.add(message.id)

    if message.content == "خط":
        await send_line(message.channel)


# 🔥 تشغيل
client.run(TOKEN)