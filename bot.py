import discord
from discord import app_commands, Activity, ActivityType
import asyncio
import os

TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
client.tree = app_commands.CommandTree(client)

# 🟢 الرومات
enabled_channels = set()
reaction_channels = set()

GUILD_ID = 935959922317860934

# 🟢 الخط الثابت
LINE_TEXT = "<https://cdn.discordapp.com/attachments/1495165123789062324/1495898310765056072/Picsart_26-04-19_17-16-50-332.jpg?ex=69e7eb5d&is=69e699dd&hm=b79859a6697d61daa33d8ad9ebed0185885dc8161c37c017a48362bd0cd9b8bd>"

# 🟢 منع التكرار النهائي
processed_messages = set()


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


# 🟢 روم بدون رياكشن
@client.tree.command(name="setchannel", description="تفعيل الخط بدون رياكشن")
async def setchannel(interaction: discord.Interaction):
    enabled_channels.add(interaction.channel.id)
    reaction_channels.discard(interaction.channel.id)
    await interaction.response.send_message("✅ تم التفعيل بدون رياكشن")


# 🟢 روم مع رياكشن
@client.tree.command(name="setchannel_reaction", description="تفعيل الخط مع رياكشن")
async def setchannel_reaction(interaction: discord.Interaction):
    reaction_channels.add(interaction.channel.id)
    enabled_channels.discard(interaction.channel.id)
    await interaction.response.send_message("💖 تم التفعيل مع رياكشن")


# 🟢 إيقاف
@client.tree.command(name="removechannel", description="إيقاف الخط")
async def removechannel(interaction: discord.Interaction):
    enabled_channels.discard(interaction.channel.id)
    reaction_channels.discard(interaction.channel.id)
    await interaction.response.send_message("❌ تم الإيقاف")


# 🟢 عرض الخط
@client.tree.command(name="line", description="عرض الخط")
async def line(interaction: discord.Interaction):
    await interaction.response.send_message(LINE_TEXT)


# 🟢 الأحداث
@client.event
async def on_message(message):
    if message.author.bot:
        return

    # 🟢 منع التكرار الحقيقي
    if message.id in processed_messages:
        return

    processed_messages.add(message.id)

    # 🟢 أمر خط
    if message.content == "خط":
        if message.author.guild_permissions.administrator:
            await message.channel.send(LINE_TEXT)
        else:
            await message.channel.send("🚫 ما عندك صلاحية")
        return

    # 🟢 بدون رياكشن
    if message.channel.id in enabled_channels:
        await message.channel.send(LINE_TEXT)
        return

    # 🟢 مع رياكشن
    if message.channel.id in reaction_channels:
        try:
            await message.add_reaction("<a:Cloude_Rose:1495925679219277864>")
        except:
            pass

        await message.channel.send(LINE_TEXT)
        return


client.run(TOKEN)