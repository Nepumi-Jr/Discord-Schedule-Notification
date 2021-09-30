from logging import disable
import os
import configparser
from discord.ext import commands
import discord
from discord.activity import Activity, ActivityType
from discord_components import Select, Button, DiscordComponents, interaction, ActionRow, SelectOption
from discord_components.component import ButtonStyle


from src.printUtil import *
from src.cmdUtil import *
from src import discordData as dData
from src.backend import handle as sData
from src import dialogFlow as dFlow

bot = commands.Bot(command_prefix="!")
DiscordComponents(bot)


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


@bot.event
async def on_guild_join(guild):
    await guild.system_channel.send("กราบสวัสดีพ่อแม่พี่น้องครับ")


@bot.event
async def on_message(mes: discord.message.Message):

    if mes.author.id == bot.user.id:
        return

    thisChannelID = mes.channel.id
    curState = dData.getState(thisChannelID)

    # !+schedule
    if mes.content.strip().lower().startswith("!+schedule"):
        await dFlow.callFlow("callSchedule", bot, thisChannelID)

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

    elif curState == "Add_Sub" or curState == "Add_Sub2":
        curSubject = mes.content.strip().replace("\n", "")
        if len(curSubject) > 20:
            curSubject = curSubject[:20] + "..."
        if curSubject:
            if curState == "Add_Sub":
                await dFlow.callFlow("Add_Link", bot, thisChannelID, curSubject)
            else:
                await dFlow.callFlow("Add_SubConBP", bot, thisChannelID, curSubject)

    elif curState == "Add_Link":
        curLink = mes.content.strip()
        if len(curLink) > 100:
            curLink = curLink[:100]
        if curLink[0] == "<" and curLink[-1] == ">":
            curLink = curLink[1:-1]
        if curLink:
            await dFlow.callFlow("Add_SubCon", bot, thisChannelID, curLink)

    elif curState == "Add_NewTime":
        curTime = mes.content.strip()
        res = timeDetection(curTime)
        print(curTime, res)
        if len(res) != 2:
            await mes.channel.send(
                f"กรุณาใส่เวลาที่ถูกต้อง เช่น `{random.randint(0,23)}:{random.randint(0,59)}`")
        else:
            await dFlow.callFlow("Add_NewTimeCon", bot, thisChannelID, list(res))


@bot.event
async def on_button_click(inter: interaction.Interaction):
    thisChannelID = inter.channel_id
    thisButtonId = inter.custom_id
    curState = dData.getState(thisChannelID)
    curChan = bot.get_channel(thisChannelID)

    pKey = dData.getStateKey(thisChannelID) + ":"
    if thisButtonId.startswith(pKey):
        thisButtonId = thisButtonId[6:]

    if thisButtonId == "deleteChanButton":
        await dFlow.callFlow("deleteChan", bot, thisChannelID)

    elif thisButtonId == "reloadButton" and curState == "idle":
        await dFlow.callFlow("justReload", bot, thisChannelID)

    elif thisButtonId == "FreloadButton":
        await dFlow.callFlow("forceReload", bot, thisChannelID)

    elif thisButtonId == "addButton" and curState == "idle":
        await dFlow.callFlow("Add_SelSub", bot, thisChannelID)

    elif thisButtonId.startswith("add_sub_") and curState == "Add_SubCon":
        if thisButtonId.endswith("OK"):
            await dFlow.callFlow("Add_AllTime", bot, thisChannelID)
        elif thisButtonId.endswith("editSub"):
            await dFlow.callFlow("Add_Sub2", bot, thisChannelID)
        else:
            await dFlow.callFlow("Add_LinkBP", bot, thisChannelID)
    elif thisButtonId.startswith("add_time_") and curState == "Add_AllTime":
        if thisButtonId.endswith("OK"):
            await dFlow.callFlow("backToIdle", bot, thisChannelID)
        elif thisButtonId.endswith("add"):
            await dFlow.callFlow("Add_NewDay", bot, thisChannelID)

    elif thisButtonId.startswith("add_NewDay_") and curState == "Add_NewDay":
        res = int(thisButtonId[11:])
        await dFlow.callFlow("Add_NewTime", bot, thisChannelID, res)

    elif thisButtonId.startswith("add_newTimeCon_") and curState == "Add_NewTimeCon":
        if thisButtonId.endswith("OK"):
            # Insert Time
            temp = dData.getTemp(thisChannelID)
            sData.insertOfUser(
                thisChannelID, temp[2]*(24*12)+temp[3], temp[0], temp[1])

            await dFlow.callFlow("Add_AllTime", bot, thisChannelID)
        else:
            await dFlow.callFlow("Add_NewDay", bot, thisChannelID)

    await inter.respond(type=6)


@bot.event
async def on_select_option(inter: interaction.Interaction):
    thisChannelID = inter.channel_id
    thisButtonId = inter.custom_id
    pKey = dData.getStateKey(thisChannelID) + ":"
    if thisButtonId.startswith(pKey):
        thisButtonId = thisButtonId[6:]

    curState = dData.getState(thisChannelID)

    curChan = bot.get_channel(thisChannelID)
    selecting = inter.values[0]
    if thisButtonId == "add_SelectSubject":
        if selecting == "!!TheNewOneeeeeeeeeeeeeee!!":
            await dFlow.callFlow("Add_Sub", bot, thisChannelID)
        else:
            dData.setTempInd(thisChannelID, 0, selecting)
            thisLink = sData.getLinkfromSubject(thisChannelID, selecting)
            dData.setTempInd(thisChannelID, 1, thisLink)
            await dFlow.callFlow("Add_AllTime", bot, thisChannelID)
    await inter.respond(type=6)


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
