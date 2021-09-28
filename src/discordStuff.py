import os
import configparser
import discord
from discord.activity import Activity, ActivityType
from src.printUtil import *

intents = discord.Intents.default()
intents.members = True


client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    botActivity = Activity(
        name="เริ่มต้นการใช้งาน โดยการพิมพ์ !+schedule ในช่องแชทที่ต้องการ (แชทส่วนตัวก็ได้)", type=ActivityType.playing)
    await client.change_presence(activity=botActivity)
    # TODO : Create Task
    # client.loop.create_task(cmd.botStatus(client))


@client.event
async def on_guild_join(guild):
    await guild.system_channel.send("กราบสวัสดีพ่อแม่พี่น้องครับ")


@client.event
async def on_message(mes: discord.message.Message):
    print(mes.channel.id)


thisToken = "???"

# ? read Config
if not os.path.exists("BigConfig.ini"):
    printError("BigConfig", "BigConfig.ini not found :(")
    exit(1)
thisConfig = configparser.ConfigParser()
thisConfig.read("BigConfig.ini")

thisToken = thisConfig["KeyToken"]["botToken"].strip()


def runBot():
    try:
        client.run(thisToken)
    except:
        print(f"Wrong Token or Fucked up\nhere is token:{thisToken}")
        exit(1)
