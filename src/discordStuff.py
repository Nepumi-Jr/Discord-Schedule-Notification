from logging import disable
import os
import configparser
from discord.ext import commands
import discord
from discord import Status
from discord.activity import Activity, ActivityType
from discord_components import Select, Button, DiscordComponents, interaction, ActionRow, SelectOption
from discord_components.component import ButtonStyle
import asyncio
import time

from src.printUtil import *
from src.cmdUtil import *
from src import discordData as dData
from src.backend import handle as sData
from src.backend import hashTime
from src import dialogFlow as dFlow
from src import discordComUse as dUse

bot = commands.Bot(command_prefix="!")
DiscordComponents(bot)


thisToken = "???"

# ? read Config
if not os.path.exists("BigConfig.ini"):
    printError("BigConfig", "BigConfig.ini not found :(")
    exit(1)
thisConfig = configparser.ConfigParser()
thisConfig.read("BigConfig.ini")

thisToken = thisConfig["KeyToken"]["botToken"].strip()


async def loopTask(bot):
    isNormalAc = False
    newDayTime = (int(thisConfig["bot"]["TimeOfNewDay"].strip()), 0)
    #newDayTime = (22, 12)
    while True:
        # local not global
        epochTimeNow = int(time.time()) + \
            int(thisConfig["bot"]["GMT"].strip())*60*60
        timeNow = time.gmtime(epochTimeNow)
        if (timeNow.tm_hour >= newDayTime[0] and timeNow.tm_min >= newDayTime[1]) and \
                ((timeNow.tm_wday+1) % 7) != dData.getDayOfWeek():
            dData.setDayOfWeek((timeNow.tm_wday+1) % 7)
            dData.setDMY(timeNow.tm_mday, timeNow.tm_mon, timeNow.tm_year)
            dData.addAllServerCReload()

        # ? Reload of the day
        while not dData.isCReloadEmpty():

            isNormalAc = False
            await bot.change_presence(activity=Activity(
                name="กำลังรีโหลดวันอัตโนมัติ...", type=ActivityType.playing),
                status=Status.dnd)
            cId = dData.popCReload()
            dData.reduceVacation(cId)
            dData.setDynaTime(cId, -1)
            if dData.getVacation(cId) == 0:
                dData.setDynaDay(cId, (timeNow.tm_wday+1) % 7)

            if dData.getState(cId) == "idle":
                try:
                    await dFlow.callFlow("justReload", bot, cId)
                except Exception as e:
                    printError("Re-day", f"Error in channel {cId}...\n{e}")

        hashedTime = hashTime.hash(epochTimeNow)
        hashedTimeFake = hashedTime + 6
        if hashedTimeFake != dData.getTimeOfWeek():
            dData.setTimeOfWeek(hashedTimeFake)
            datas = sData.getTimeSubject(hashedTimeFake)
            if datas:
                for d in datas:
                    dData.pushServerSReload(d[0])

        # ? Reload of Subject
        while not dData.isSReloadEmpty():
            isNormalAc = False
            await bot.change_presence(activity=Activity(
                name="กำลังรีโหลดวิชาอัตโนมัติ...", type=ActivityType.playing),
                status=Status.dnd)
            cId = dData.popSReload()
            if dData.getVacation(cId) == 0:
                dData.setDynaTime(cId, hashedTimeFake)
            if dData.getState(cId) == "idle":
                try:
                    await dFlow.callFlow("justReload", bot, cId)
                except Exception as e:
                    printError("Re-Schedule",
                               f"Error in channel {cId}...\n{e}")

        if not isNormalAc:
            await bot.change_presence(activity=Activity(
                name="[!+schedule] เริ่มต้นการใช้งาน โดยการพิมพ์ !+schedule ในช่องแชทที่ต้องการ (แชทส่วนตัวก็ได้)", type=ActivityType.playing),
                status=Status.online)
            isNormalAc = True
        await asyncio.sleep(2)


@ bot.event
async def on_ready():
    printSuggest("Discord", "Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    # TODO : Create Task
    bot.loop.create_task(loopTask(bot))


@ bot.event
async def on_guild_join(guild):
    await guild.system_channel.send("กราบสวัสดีพ่อแม่พี่น้องครับ")


@ bot.event
async def on_message(mes: discord.message.Message):

    if mes.author.id == bot.user.id:
        return

    thisChannelID = mes.channel.id
    curState = dData.getState(thisChannelID)

    for ment in mes.mentions:
        if bot.user.name == ment.display_name:
            await mes.channel.send("เริ่มต้นการใช้งาน โดยการพิมพ์ `!+schedule` ในช่องแชทที่ต้องการเลยยยย (แชทส่วนตัวก็ได้)")

    # !+schedule
    if mes.content.strip().lower().startswith("!+schedule"):
        await dFlow.callFlow("callSchedule", bot, thisChannelID)

    elif mes.content.strip().lower().startswith("!+hello"):
        await mes.channel.send("ว่าไง")

    elif mes.content.strip().lower().startswith("!+admin"):
        passText = mes.content.replace("!+admin", "").strip()
        res = regisAdmin(str(thisChannelID), passText)
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
        if len(curLink) > 1000:
            curLink = curLink[:1000]
        if curLink[0] == "<" and curLink[-1] == ">":
            curLink = curLink[1:-1]
        if curLink:
            await dFlow.callFlow("Add_SubCon", bot, thisChannelID, curLink)

    elif curState == "Add_NewTime":
        curTime = mes.content.strip()
        res = timeDetection(curTime)
        if len(res) != 2:
            await mes.channel.send(
                f"กรุณาใส่เวลาที่ถูกต้อง เช่น `{random.randint(0,23)}:{random.randint(0,59)}`")
        else:
            await dFlow.callFlow("Add_NewTimeCon", bot, thisChannelID, list(res))

    elif curState == "Edi_ChaSub":
        curSubject = mes.content.strip().replace("\n", "")
        if len(curSubject) > 20:
            curSubject = curSubject[:20] + "..."
        if curSubject:
            oldSub = dData.getTemp(thisChannelID)[0]
            sData.changeSubject(thisChannelID, oldSub, curSubject)
            dData.setTempInd(thisChannelID, 0, curSubject)
            await dFlow.callFlow("Edi_Sub", bot, thisChannelID)

    elif curState == "Edi_ChaLink":
        curLink = mes.content.strip()
        if len(curLink) > 1000:
            curLink = curLink[:1000]
        if curLink[0] == "<" and curLink[-1] == ">":
            curLink = curLink[1:-1]
        if curLink:
            oldSubject = dData.getTemp(thisChannelID)[0]
            sData.changeLink(thisChannelID, oldSubject, curLink)
            dData.setTempInd(thisChannelID, 1, curLink)
            await dFlow.callFlow("Edi_Sub", bot, thisChannelID)

    elif curState == "Edi_ChaTimeTime":
        curTime = mes.content.strip()
        res = timeDetection(curTime)
        if len(res) != 2:
            await mes.channel.send(
                f"กรุณาใส่เวลาที่ถูกต้อง เช่น `{random.randint(0,23)}:{random.randint(0,59)}`")
        else:
            fromTimeHased = dData.getTempInd(thisChannelID, 2)
            fromTime = hashTime.hashBack(fromTimeHased)
            newTimeHashed = dData.getTempInd(
                thisChannelID, 3)*24*12 + res[0] * 12 + res[1]
            newTime = hashTime.hashBack(newTimeHashed)
            sData.changeTime(thisChannelID, fromTimeHased, newTimeHashed)
            await mes.channel.send(
                f"🔄เปลี่ยนเวลาจาก `{dUse.fromTerzTimeToStr(fromTime)}` เป็น `{dUse.fromTerzTimeToStr(newTime)}` สำเร็จ")

            await dFlow.callFlow("Edi_Sub", bot, thisChannelID)


@ bot.event
async def on_button_click(inter: interaction.Interaction):
    thisChannelID = inter.channel_id
    thisButtonId = inter.custom_id
    curState = dData.getState(thisChannelID)
    curChan = bot.get_channel(thisChannelID)
    if dData.getStateKey(thisChannelID) != 0:
        pKey = dData.getStateKey(thisChannelID) + ":"
        if thisButtonId.startswith(pKey):
            thisButtonId = thisButtonId[6:]

        if thisButtonId == "deleteChanButton":
            await dFlow.callFlow("deleteChan", bot, thisChannelID)
        elif thisButtonId == "delChan_Bye":
            await dFlow.callFlow("byebye", bot, thisChannelID)
        elif thisButtonId == "reloadButton" and curState == "idle":
            await dFlow.callFlow("justReload", bot, thisChannelID)

        elif thisButtonId == "FreloadButton":
            await dFlow.callFlow("forceReload", bot, thisChannelID)

        elif thisButtonId == "backToMenu":
            await dFlow.callFlow("backToIdle", bot, thisChannelID)

        elif thisButtonId == "scheButton" and curState == "idle":
            await dFlow.callFlow("Sche_call", bot, thisChannelID)

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

        elif thisButtonId == "editButton" and curState == "idle":
            await dFlow.callFlow("Edi_SelSub", bot, thisChannelID)
        elif thisButtonId.startswith("edit_sub_") and curState == "Edi_Sub":
            if thisButtonId.endswith("subj"):
                await dFlow.callFlow("Edi_ChaSub", bot, thisChannelID)
            elif thisButtonId.endswith("link"):
                await dFlow.callFlow("Edi_ChaLink", bot, thisChannelID)
            else:
                await dFlow.callFlow("Edi_ChaTime", bot, thisChannelID)
        elif thisButtonId == "edit_chaTimSub" and curState == "Edi_ChaTime":
            await dFlow.callFlow("Edi_Sub", bot, thisChannelID)

        elif thisButtonId.startswith("edi_chaTimeDay_") and curState == "Edi_ChaTimeDay":
            res = int(thisButtonId[15:])
            dData.setTempInd(thisChannelID, 3, res)
            await dFlow.callFlow("Edi_ChaTimeTime", bot, thisChannelID)

        # delButton
        elif thisButtonId == "delButton" and curState == "idle":
            await dFlow.callFlow("Rem_SelSub", bot, thisChannelID)

        elif thisButtonId.startswith("rem_allSubCon_") and curState == "Rem_AllSubCon":
            if thisButtonId.endswith("Remove"):
                sData.delAllTime(thisChannelID)
                await curChan.send("💥ลบเรียบร้อยแล้ว...")
                await dFlow.callFlow("backToIdle", bot, thisChannelID)
            else:
                await dFlow.callFlow("Rem_SelSub", bot, thisChannelID)

        elif thisButtonId.startswith("rem_sub_") and curState == "Rem_Sub":
            if thisButtonId.endswith("back"):
                await dFlow.callFlow("Rem_SelSub", bot, thisChannelID)
            elif thisButtonId.endswith("subj"):
                await dFlow.callFlow("Rem_SubCon", bot, thisChannelID)
            else:
                await dFlow.callFlow("Rem_SelTimeSub", bot, thisChannelID)

        elif thisButtonId.startswith("rem_subCon_") and curState == "Rem_SubCon":
            if thisButtonId.endswith("Remove"):
                thisSub = dData.getTempInd(thisChannelID, 0)
                sData.delSubject(thisChannelID, thisSub)
                await curChan.send(f"💥ลบวิชา `{thisSub}` แล้ว")
                if sData.isExistId(thisChannelID):
                    await dFlow.callFlow("Rem_SelSub", bot, thisChannelID)
                else:
                    await dFlow.callFlow("backToIdle", bot, thisChannelID)
            else:
                await dFlow.callFlow("Rem_Sub", bot, thisChannelID)

        elif thisButtonId == "rem_selTimeSub_back":
            await dFlow.callFlow("Rem_Sub", bot, thisChannelID)

        elif thisButtonId == "toggleNoToday" and curState == "idle":
            await dFlow.callFlow("tog_vaca", bot, thisChannelID,
                                 (dData.getVacation(thisChannelID) == 0))

        elif thisButtonId == "togNoti" and curState == "idle":
            await dFlow.callFlow("tog_noti", bot, thisChannelID)

        try:
            await inter.respond(type=6)
        except:
            pass


@ bot.event
async def on_select_option(inter: interaction.Interaction):
    thisChannelID = inter.channel_id
    thisButtonId = inter.custom_id
    if dData.getStateKey(thisChannelID) != 0:
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
        elif thisButtonId == "edi_SelectSubject":
            dData.setTempInd(thisChannelID, 0, selecting)
            thisLink = sData.getLinkfromSubject(thisChannelID, selecting)
            dData.setTempInd(thisChannelID, 1, thisLink)
            await dFlow.callFlow("Edi_Sub", bot, thisChannelID)
        elif thisButtonId == "edit_chaTime":
            dData.setTempInd(thisChannelID, 2, int(selecting))
            await dFlow.callFlow("Edi_ChaTimeDay", bot, thisChannelID)
        elif thisButtonId == "rem_SelectSubject":
            if selecting == "!!RRREEEEMMMMOOvEEEEEEALL!!!":
                await dFlow.callFlow("Rem_AllSubCon", bot, thisChannelID)
            else:
                dData.setTempInd(thisChannelID, 0, selecting)
                thisLink = sData.getLinkfromSubject(thisChannelID, selecting)
                dData.setTempInd(thisChannelID, 1, thisLink)
                await dFlow.callFlow("Rem_Sub", bot, thisChannelID)

        elif thisButtonId == "rem_selTimeSub_rem":
            sData.delByTime(thisChannelID, int(selecting))
            await curChan.send(
                f"💥ลบ `{dUse.fromTerzTimeToStr(hashTime.hashBack(int(selecting)))}` แล้ว")
            thisSubs = sData.getallSubjects(thisChannelID)
            if dData.getTempInd(thisChannelID, 0) in thisSubs:
                await dFlow.callFlow("Rem_Sub", bot, thisChannelID)
            else:
                await dFlow.callFlow("Rem_SelSub", bot, thisChannelID)

        elif thisButtonId == "tog_vaca":
            day = int(selecting)
            dData.setVacation(thisChannelID, day)
            await curChan.send(
                f"🎉ว้าว ไม่มีเรียน {day} วัน!!")
            await dFlow.callFlow("backToIdle", bot, thisChannelID)

        try:
            await inter.respond(type=6)
        except:
            pass


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
