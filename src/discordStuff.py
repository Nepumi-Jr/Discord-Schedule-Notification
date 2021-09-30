from logging import disable
import os
import configparser
from discord.ext import commands
import discord
from discord.activity import Activity, ActivityType
from discord_components import Select, Button, DiscordComponents, interaction, ActionRow
from discord_components.component import ButtonStyle


from src.printUtil import *
from src import discordData as dData
from src.cmdUtil import *
from src.backend import handle as sData

bot = commands.Bot(command_prefix="!")
DiscordComponents(bot)


async def getMessage(chaID, messID):
    try:
        cha = await bot.fetch_channel(chaID)
    except:
        return None

    try:
        mess = await cha.fetch_message(messID)
    except:
        return None

    return mess


async def doDeleteLastCMDMessage(thisChannelID):
    try:
        lastMessage = await getMessage(
            thisChannelID, dData.getMessID(thisChannelID))
        await lastMessage.delete()
    except:
        pass


@bot.event
async def on_ready():
    printSuggest("Discord", "Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    botActivity = Activity(
        name="เริ่มต้นการใช้งาน โดยการพิมพ์ !+schedule ในช่องแชทที่ต้องการ (แชทส่วนตัวก็ได้)", type=ActivityType.playing)
    await bot.change_presence(activity=botActivity)
    # TODO : Create Task
    # client.loop.create_task(cmd.botStatus(client))


def getMenuComponents():
    return [
        ActionRow(
            Button(
                label="เพิ่มรายวิชา/เวลา",
                custom_id="addButton",
                style=ButtonStyle.green,
                emoji="➕"),
            Button(
                label="แก้ไขรายวิชา/เวลา",
                custom_id="editButton",
                style=ButtonStyle.gray,
                emoji="🔨",
                disabled=True),
            Button(
                label="ลบรายวิชา/เวลา",
                custom_id="delButton",
                style=ButtonStyle.red,
                emoji="❌",
                disabled=True),
        ),
        ActionRow(
            Button(
                label="ตั้งค่าการใช้งาน",
                custom_id="settingButton",
                style=ButtonStyle.gray,
                emoji="🔧",
                disabled=True),
            Button(
                label="รีโหลด",
                custom_id="reloadButton",
                style=ButtonStyle.blue,
                emoji="🔁"),
            Button(
                label="เริ่มต้นการทำงานใหม่",
                custom_id="FreloadButton",
                style=ButtonStyle.red,
                emoji="⚠"),
            Button(
                label="ตรวจสอบเวอร์ชั่น",
                custom_id="checkVersion",
                style=ButtonStyle.gray,
                emoji="⏫",
                disabled=True),
        ),
        ActionRow(
            Button(
                label="ลบแชลเนลนี้(ข้อมูลจะหายทั้งหมด!!!)",
                custom_id="deleteChanButton",
                style=ButtonStyle.red,
                emoji="💥"),
            Button(
                label="น่ า ส น ใ จ",
                style=ButtonStyle.URL,
                url="https://www.youtube.com/watch?v=iik25wqIuFo",
                emoji="❔"),
        )

    ]


async def menuCmdCommand(chan):
    return await chan.send(":clock1:**ยินดีต้อนรับสู่การใช้งาน บอทขอลิงก์(ห้อง)เรียน**:clock1:\n \\* สามารถใช้ปุ่มด้านล่างนี้ในการควบคุมต่าง ๆ\n*แนะนำ : ไม่ควรใช้ห้องแชทนี้ในการสนทนาปกติ*",
                           components=getMenuComponents())


@bot.event
async def on_guild_join(guild):
    await guild.system_channel.send("กราบสวัสดีพ่อแม่พี่น้องครับ")


@bot.event
async def on_message(mes: discord.message.Message):

    if mes.author.id == bot.user.id:
        return

    thisChannelID = mes.channel.id

    # !+schedule
    if mes.content.strip().lower().startswith("!+schedule"):

        thisMes = await menuCmdCommand(mes.channel)

        if dData.isExistID(thisChannelID):
            await doDeleteLastCMDMessage(thisChannelID)
            dData.setMessID(thisChannelID, thisMes.id)
        else:
            dData.createNewID(thisChannelID, thisMes.id)

    elif mes.content.strip().lower().startswith("!+hello"):
        await mes.channel.send("ว่าไง")

    elif mes.content.strip().lower().startswith("!+admin"):
        passText = mes.content.replace("!+admin", "").strip()
        res = regisAdmin(str(thisChannelID), passText)
        print("pass:", passText)
        print(isAdmin(str(thisChannelID)))
        if res == 1:
            await mes.channel.send(
                ":computer:**ยินดีต้อนรับ Adminnnnnnn**:computer:\nลองใช้คำสั่ง `!+help` ในการดูว่าแอดมินสามารถใช้คำสั่งอะไรได้บ้าง")
        elif res == 2:
            await mes.channel.send(
                "คุณเป็น admin อยู่แล้วววววววว\nลองใช้คำสั่ง `!+help` ในการดูว่าแอดมินสามารถใช้คำสั่งอะไรได้บ้าง")


@bot.event
async def on_button_click(inter: interaction.Interaction):
    thisChannelID = inter.channel_id
    thisButtonId = inter.custom_id
    await inter.respond(type=6)
    if thisButtonId == "deleteChanButton":
        if dData.isExistID(thisChannelID):
            await doDeleteLastCMDMessage(thisChannelID)
            dData.removeID(thisChannelID)
            await bot.get_channel(thisChannelID).send(":boom:**ลบแชลเนลเรียบร้อย**:boom:\nหวังว่าจะได้ให้บริการอีกครั้ง *(ซึม...)*")
        else:
            await bot.get_channel(thisChannelID).send("เ ป็ น ไ ป ไ ม่ ไ ด้")

    elif thisButtonId == "reloadButton":
        await doDeleteLastCMDMessage(thisChannelID)
        thisMes = await menuCmdCommand(inter.channel)
        dData.setMessID(thisChannelID, thisMes.id)

    elif thisButtonId == "FreloadButton":
        await bot.get_channel(thisChannelID).send("-"*20)
        dData.setState(thisChannelID, "idle")
        dData.setTemp(thisChannelID, [])
        await bot.get_channel(thisChannelID).send("🔁เริ่มต้นระบบใหม่🔁")
        await doDeleteLastCMDMessage(thisChannelID)
        thisMes = await menuCmdCommand(inter.channel)
        dData.setMessID(thisChannelID, thisMes.id)

    elif thisButtonId == "addButton":
        subjects = sData.getallSubjects(thisChannelID)
        # Select exist subject or Add new one


thisToken = "???"

# ? read Config
if not os.path.exists("BigConfig.ini"):
    printError("BigConfig", "BigConfig.ini not found :(")
    exit(1)
thisConfig = configparser.ConfigParser()
thisConfig.read("BigConfig.ini")

thisToken = thisConfig["KeyToken"]["botToken"].strip()


def runBot():
    printSuggest("Discord", "Loading data...")
    try:
        dData.loadData()
        sData.loadData()
    except Exception as e:
        printError("Discord", f"Fail to load data...")
        print(e)
        exit(1)

    printSuggest("Discord", "Runing bot...")
    try:
        bot.run(thisToken)
    except Exception as e:
        printError(
            "Discord", f"Wrong Token or Fucked up\nhere is token:{thisToken}")
        print(e)
        exit(1)
