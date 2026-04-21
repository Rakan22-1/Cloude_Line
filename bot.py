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

# 🟢 منع التكرار (قفل قوي)
last_trigger = {}

# 🟢 الصورة الثابتة
IMAGE_URL = "https://cdn.discordapp.com/attachments/1495165123789062324/1495898310765056072/Picsart_26-04-19_17-16-50-332.jpg?ex=69e7eb5d&is=69e699dd&hm=b79859a6697d61daa33d8ad9ebed0185885dc8161c37c017a48362bd0cd9b8bd"


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


# 🟢 عرض الخط (صورة)
@client.tree.command(name="line", description="عرض الخط")
async def line(interaction: discord.Interaction):

    embed = discord.Embed()
    embed.set_image(url=IMAGE_URL)

    await interaction.response.send_message(embed=embed)


# 🟢 منع التكرار القوي
@client.event
async def on_message(message):
    if message.author.bot:
        return

    key = message.channel.id

    if key in last_trigger:
        return

    last_trigger[key] = True
    asyncio.create_task(remove_lock(key))

    # 🟢 أمر خط
    if message.content == "خط":
        if message.author.guild_permissions.administrator:
            await send_line(message.channel)
        else:
            await message.channel.send("🚫 ما عندك صلاحية")
        return

    # 🟢 بدون رياكشن
    if message.channel.id in enabled_channels:
        await send_line(message.channel)
        return

    # 🟢 مع رياكشن
    if message.channel.id in reaction_channels:
        try:
            await message.add_reaction("<a:Cloude_Rose:1495925679219277864>")
        except:
            pass

        await send_line(message.channel)
        return


# 🟢 إرسال الخط (Embed)
async def send_line(channel):
    embed = discord.Embed()
    embed.set_image(url=IMAGE_URL)
    await channel.send(embed=embed)


# 🟢 فك القفل
async def remove_lock(key):
    await asyncio.sleep(1)
    last_trigger.pop(key, None)


client.run(TOKEN)