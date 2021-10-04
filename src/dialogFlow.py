from random import choice
from discord.colour import Color
from discord.embeds import Embed
from discord_components import Select, Button, DiscordComponents, interaction, ActionRow, SelectOption
from discord_components.component import ButtonStyle

from src import discordData as dData
from src.backend import handle as sData
from src.backend import hashTime
from src import cmdUtil as util
from src import discordComUse as dUse

VERSION = "เวอร์ชั่น Beta 1.0.2 (แก้ไข 4 ต.ค. 64)"

dayInThai = ["อาทิตย์", "จันทร์", "อังคาร",
             "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์"]
dayColor = [Color.red(), Color.gold(), Color.magenta(),
            Color.green(), Color.orange(), Color.blue(), Color.purple()]
monthInThai = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน",
               "พฤษภาคม ", "มิถุนายน", "กรกฎาคม", "สิงหาคม",
               "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
randomWord = ["สวัสดี วัน<day>", "วัน<day> เป็นวันที่ดีย์"]


async def getMessage(bot, chaID, messID):
    try:
        cha = await bot.fetch_channel(chaID)
    except:
        return None

    try:
        mess = await cha.fetch_message(messID)
    except:
        return None

    return mess


async def doDeleteLastCMDMessage(bot, thisChannelID):
    try:
        lassIdNoti = dData.getNotiMessID(thisChannelID)
        if lassIdNoti != -1:
            lastMessage = await getMessage(bot, thisChannelID, lassIdNoti)
            await lastMessage.delete()
    except:
        pass

    try:
        lastMessage = await getMessage(bot, thisChannelID, dData.getMessID(thisChannelID))
        await lastMessage.delete()
    except:
        pass


async def delAllPrevMess(bot, thisChannelID):
    datas = dData.getPrevMess(thisChannelID)
    for m in datas:
        try:
            lastMessage = await getMessage(bot, thisChannelID, m)
            await lastMessage.delete()
        except:
            pass
    dData.clearPrevMess(thisChannelID)


async def messageOfContent(chan):
    thisChanId = chan.id
    dyna = dData.getDyna(thisChanId)
    if dyna == -1:
        return None
    elif dyna[1] == -1:
        return None

    if dyna[0] == "Day":
        dayOfTheWeek = dyna[1]
        thisMenuEmbed = Embed(
            title=f"วัน{dayInThai[dayOfTheWeek]}",
            description=f"มีทั้งหมด {sData.getNSubjectOfDay(thisChanId,dayOfTheWeek)} วิชาในวันนี้",
            colour=dayColor[dayOfTheWeek])

        datas = sData.getSubjectOfDay(thisChanId, dayOfTheWeek)
        for d in datas:
            thisMenuEmbed.add_field(
                name=f"[{dUse.fromTerzTimeToStr(hashTime.hashBack(d[0]))}] {d[1][0]}", value=str(d[1][1]), inline=False)
        return await chan.send(embed=thisMenuEmbed)
    else:
        timeHased = dyna[1]
        dayOfTheWeek = dData.getDayOfWeek()
        datas = sData.getDataFromTimeUser(thisChanId, timeHased)
        thisMenuEmbed = Embed(
            title=f"{datas[0]}",
            description=f"{dUse.fromTerzTimeToStr(hashTime.hashBack(timeHased))}",
            colour=dayColor[dayOfTheWeek])
        thisMenuEmbed.add_field(name="ลิ้ง", value=datas[1])

        try:
            x = await chan.send(embed=thisMenuEmbed, components=[
                Button(
                    label="ลิ้งเรียน",
                    style=ButtonStyle.URL,
                    url=datas[1],
                    emoji="🔗"
                )
            ])
        except:
            x = await chan.send(embed=thisMenuEmbed)
        return x


async def menuCmdCommand(chan):
    thisChanId = chan.id
    dayOfWeek = dData.getDayOfWeek()
    if dayOfWeek == -1:
        return await chan.send(":clock1:**ยินดีต้อนรับสู่การใช้งาน บอทขอลิงก์(ห้อง)เรียน**:clock1:\n \\* สามารถใช้ปุ่มด้านล่างนี้ในการควบคุมต่าง ๆ\n*แนะนำ : ไม่ควรใช้ห้องแชทนี้ในการสนทนาปกติ*",
                               components=dUse.getMenuComponents(thisChanId))
    else:
        date = dData.getDMY()
        thisMenuEmbed = Embed(
            title=choice(randomWord).replace("<day>", dayInThai[dayOfWeek]),
            description=f"วันที่ {date[0]} {monthInThai[date[1]-1]} ปี {date[2]+543}",
            colour=dayColor[dayOfWeek])
        thisMenuEmbed.add_field(name="📚 จำนวนวิชาที่อยู่ในระบบ",
                                value=f"ทั้งหมด {sData.getNSubject(thisChanId)} วิชา")
        thisMenuEmbed.add_field(name="📕 จำนวนวิชาในวันนี้",
                                value=f"มี {sData.getNSubjectOfDay(thisChanId,dayOfWeek)} วิชา")
        thisMenuEmbed.add_field(name="💬 โหมดการแจ้งเตือน", value=dData.isNotiDay(
            thisChanId) and "เตือนทุก ๆ วัน" or "เตือนทุก ๆ วิชา")
        thisMenuEmbed.add_field(name="🏖 หยุดเรียนหรือไม่", value=dData.getVacation(
            thisChanId) == 0 and "เรียนตามปกติ" or f"วู้ว หยุดอีก {dData.getVacation(thisChanId)} วัน")
        thisMenuEmbed.set_footer(text=VERSION)

        return await chan.send(":clock1:**ยินดีต้อนรับสู่การใช้งาน บอทขอลิงก์(ห้อง)เรียน**:clock1:\n \\* สามารถใช้ปุ่มด้านล่างนี้ในการควบคุมต่าง ๆ\n*แนะนำ : ไม่ควรใช้ห้องแชทนี้ในการสนทนาปกติ*",
                               embed=thisMenuEmbed,
                               components=dUse.getMenuComponents(thisChanId))


async def callFlow(idFlow, bot, thisChannelID, dlcc=None):
    global dayInThai
    thisChannel = await bot.fetch_channel(thisChannelID)
    if idFlow == "callSchedule":
        if dData.isExistID(thisChannelID):
            # Like reset
            dData.setState(thisChannelID, "idle")
            dData.makeNewKey(thisChannelID)
            dData.setTemp(thisChannelID, [])
            await doDeleteLastCMDMessage(bot, thisChannelID)
            thisMes = await messageOfContent(thisChannel)
            if thisMes:
                dData.setNotiMessID(thisChannelID, thisMes.id)
            thisMes = await menuCmdCommand(thisChannel)
            dData.setMessID(thisChannelID, thisMes.id)
        else:
            thisMes = await messageOfContent(thisChannel)
            if thisMes:
                dData.setNotiMessID(thisChannelID, thisMes.id)
            thisMes = await menuCmdCommand(thisChannel)
            dData.createNewID(thisChannelID, thisMes.id)
    elif idFlow == "deleteChan":
        if dData.isExistID(thisChannelID):
            dData.setState(thisChannelID, "delChan_Con")
            pKey = dData.makeNewKey(thisChannelID) + ":"
            thisEmbed = Embed(title="สิ่งที่จะหายไป",
                              description="ห า ย ไ ป", colour=Color.dark_red())
            thisEmbed.add_field(
                name="ข้อมูลตาราง", value="ตารางจะหายไปทั้งหมด และหากสร้างใหม่ ข้อมูลเก่าจะไม่กู้คืน(กรอกใหม่)", inline=False)
            thisEmbed.add_field(name="การตั้งค่า",
                                value="การตั้งค่าจะหายไป", inline=False)
            m = await thisChannel.send("**💥💥คุณกำลังจะลบแชลเนลนี้💥💥**\nหากลบแล้ว จะไม่สามารถกู้คืนได้ แน่ใจแล้วหรือไม่",
                                       embed=thisEmbed,
                                       components=[ActionRow(
                                           Button(
                                               label="แน่ใจแล้วที่จะลบทิ้ง!!!",
                                               custom_id=pKey + "delChan_Bye",
                                               style=ButtonStyle.red,
                                               emoji="💥"),
                                           dUse.backToMenu(pKey)
                                       )])
            dData.addMessageId(thisChannelID, m.id)
        else:
            await thisChannel.send("เ ป็ น ไ ป ไ ม่ ไ ด้")
    elif idFlow == "byebye":
        dData.makeNewKey()
        await doDeleteLastCMDMessage(bot, thisChannelID)
        await delAllPrevMess(bot, thisChannelID)
        dData.removeID(thisChannelID)
        sData.delAllTime(thisChannelID)
        await thisChannel.send(":boom:**ลบแชลเนลเรียบร้อย**:boom:\nหวังว่าจะได้ให้บริการอีกครั้ง *(ซึม...)*")
    elif idFlow == "justReload":
        await doDeleteLastCMDMessage(bot, thisChannelID)
        thisMes = await messageOfContent(thisChannel)
        if thisMes:
            dData.setNotiMessID(thisChannelID, thisMes.id)
        thisMes = await menuCmdCommand(thisChannel)
        dData.setMessID(thisChannelID, thisMes.id)
    elif idFlow == "forceReload":
        await thisChannel.send("-"*50)
        dData.setState(thisChannelID, "idle")
        dData.makeNewKey(thisChannelID)
        dData.setTemp(thisChannelID, [])
        await thisChannel.send("🔁เริ่มต้นระบบใหม่🔁")
        await doDeleteLastCMDMessage(bot, thisChannelID)
        thisMes = await messageOfContent(thisChannel)
        if thisMes:
            dData.setNotiMessID(thisChannelID, thisMes.id)
        thisMes = await menuCmdCommand(thisChannel)
        dData.setMessID(thisChannelID, thisMes.id)
    elif idFlow == "backToIdle":
        await delAllPrevMess(bot, thisChannelID)
        dData.setState(thisChannelID, "idle")
        dData.setTemp(thisChannelID, [])
        dData.makeNewKey(thisChannelID)
        await doDeleteLastCMDMessage(bot, thisChannelID)
        thisMes = await messageOfContent(thisChannel)
        if thisMes:
            dData.setNotiMessID(thisChannelID, thisMes.id)
        thisMes = await menuCmdCommand(thisChannel)
        dData.setMessID(thisChannelID, thisMes.id)

    elif idFlow == "Sche_call":

        for i in range(7):
            dayOfTheWeek = i
            datas = sData.getSubjectOfDay(thisChannelID, dayOfTheWeek)
            if datas:
                thisMenuEmbed = Embed(
                    title=f"วัน{dayInThai[dayOfTheWeek]}",
                    description=f"มีทั้งหมด {len(datas)} วิชาในวันนี้",
                    colour=dayColor[dayOfTheWeek])

                for d in datas:
                    thisMenuEmbed.add_field(
                        name=f"[{dUse.fromTerzTimeToStr(hashTime.hashBack(d[0]))}] {d[1][0]}", value=str(d[1][1]), inline=False)
                await thisChannel.send(embed=thisMenuEmbed)

        await callFlow("justReload", bot, thisChannelID)

    # ? ADDD

    elif idFlow == "Add_SelSub":
        dData.setState(thisChannelID, "Add_SelSub")
        pKey = dData.makeNewKey(thisChannelID) + ":"
        m = await thisChannel.send("**+ เพิ่มรายวิชา / เวลา +**\nกรุณาเลือกวิชาที่จะเพิ่มเวลาหรือเพิ่มวิชา",
                                   components=[
                                       dUse.makeSelectSubject(
                                           thisChannelID, pKey+"add_SelectSubject",
                                           [("+ เพิ่มวิชาใหม่", "!!TheNewOneeeeeeeeeeeeeee!!", "➕")]),
                                       dUse.backToMenu(pKey)
                                   ])
        dData.addMessageId(thisChannelID, m.id)
    elif idFlow == "Add_Sub" or idFlow == "Add_Sub2":
        await delAllPrevMess(bot, thisChannelID)
        dData.setState(thisChannelID, idFlow)
        await thisChannel.send(":speech_balloon:กรุณาใส่ชื่อวิชาที่จะต้องการเพิ่ม (ไม่เกิน 20 ตัวอักษร)\n*ส่งมาในแชทนี้เลย*")

    elif idFlow == "Add_Link" or idFlow == "Add_LinkBP":
        # * Use dlc as curSubject
        if idFlow == "Add_Link":
            curSubject = dlcc
            dData.setTempInd(thisChannelID, 0, curSubject)
        else:
            curSubject = dData.getTemp(thisChannelID)[0]

        dData.setState(thisChannelID, "Add_Link")
        await thisChannel.send(
            f":closed_book: **วิชา `{curSubject}`**\n:speech_balloon: กรุณาใส่ลิ้งเรียนเลย\n*ขอแค่ลิ้งก็พอ*")

    elif idFlow == "Add_SubCon" or idFlow == "Add_SubConBP":
        await delAllPrevMess(bot, thisChannelID)
        if idFlow == "Add_SubCon":
            # * Use dlc as curLink
            curLink = dlcc
            dData.setTempInd(thisChannelID, 1, curLink)
            newTemp = dData.getTemp(thisChannelID)
        else:
            # * Use dlc as curSubject
            curSubject = dlcc
            newTemp = dData.getTemp(thisChannelID)
            newTemp[0] = curSubject
            dData.setTemp(thisChannelID, newTemp)
        pKey = dData.makeNewKey(thisChannelID) + ":"
        dData.setState(thisChannelID, "Add_SubCon")

        menus = ActionRow(
            dUse.acceptButton(pKey+"add_sub_OK"),
            dUse.anyButton(pKey+"add_sub_editSub", "แก้ไขชื่อวิชา", "📕"),
            dUse.anyButton(pKey+"add_sub_editLink", "แก้ไขลิ้ง", "🔗"),
        )
        try:
            m = await thisChannel.send(
                f"**กรอกข้อมูลวิชาสำเร็จ**\nหน้าตาจะออกมาเป็นแบบนี้",
                embed=Embed(
                    title=newTemp[0],
                    description=newTemp[1], colour=Color.random()),
                components=[ActionRow(
                    Button(
                        label="ลิ้งเรียน",
                        style=ButtonStyle.URL,
                        url=newTemp[1],
                        emoji="🔗")
                ), menus])
        except:
            m = await thisChannel.send(
                f"**กรอกข้อมูลวิชาสำเร็จ**\nหน้าตาจะออกมาเป็นแบบนี้",
                embed=Embed(
                    title=newTemp[0],
                    description=newTemp[1], colour=Color.random()),
                components=[menus])
        dData.addMessageId(thisChannelID, m.id)

    elif idFlow == "Add_AllTime":
        await delAllPrevMess(bot, thisChannelID)
        dData.setState(thisChannelID, "Add_AllTime")
        newTemp = dData.getTemp(thisChannelID)
        pKey = dData.makeNewKey(thisChannelID) + ":"
        thisEm = dUse.getEmbedAllTimeFromSubject(
            thisChannelID, newTemp[0], newTemp[1])
        m = await thisChannel.send(
            f"**ตารางเวลาของวิชานี้...**",
            embed=thisEm,
            components=[ActionRow(
                dUse.backToMenu(pKey),
                dUse.anyButton(pKey+"add_time_add", "เพิ่มเวลาเรียน", "🕒")
            )])
        dData.addMessageId(thisChannelID, m.id)

    elif idFlow == "Add_NewDay":
        await delAllPrevMess(bot, thisChannelID)
        dData.setState(thisChannelID, "Add_NewDay")
        pKey = dData.makeNewKey(thisChannelID) + ":"
        dayInThai = ["อาทิตย์", "จันทร์", "อังคาร",
                     "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์"]
        m = await thisChannel.send(
            f":calendar_spiral:**กรุณาเลือกวันที่เรียน**:calendar_spiral:",
            components=[ActionRow(
                dUse.anyButton(pKey+"add_NewDay_0", "วัน"+dayInThai[0], "🕒"),
                dUse.anyButton(pKey+"add_NewDay_1", "วัน"+dayInThai[1], "🕒"),
                dUse.anyButton(pKey+"add_NewDay_2", "วัน"+dayInThai[2], "🕒")),
                ActionRow(
                dUse.anyButton(pKey+"add_NewDay_3", "วัน"+dayInThai[3], "🕒"),
                dUse.anyButton(pKey+"add_NewDay_4", "วัน"+dayInThai[4], "🕒"),
                dUse.anyButton(pKey+"add_NewDay_5", "วัน"+dayInThai[5], "🕒"),
                dUse.anyButton(pKey+"add_NewDay_6", "วัน"+dayInThai[6], "🕒"),
            )])
        dData.addMessageId(thisChannelID, m.id)

    elif idFlow == "Add_NewTime":
        await delAllPrevMess(bot, thisChannelID)
        dData.setTempInd(thisChannelID, 2, dlcc)
        ttemp = dData.getTemp(thisChannelID)
        dData.setState(thisChannelID, "Add_NewTime")
        dayInThai = ["อาทิตย์", "จันทร์", "อังคาร",
                     "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์"]

        await thisChannel.send(
            f":clock3:วิชา `{ttemp[0]}` ในทุก ๆ `วัน{dayInThai[dlcc]}` ตอนกี่โมง??\n" +
            "* - ใส่เป็นเวลา `xx:xx` มาที่แชทนี้เลย*\n" +
            "* - เวลาจะรับได้แค่เวลาที่หารด้วย 5 ลงตัว เช่น 0:00 0:05 0:10 เป็นต้น*")

    elif idFlow == "Add_NewTimeCon":
        dData.setTempInd(thisChannelID, 3, dlcc[0]*12 + dlcc[1]//5)
        curTemp = dData.getTemp(thisChannelID)
        pKey = dData.makeNewKey(thisChannelID) + ":"
        dData.setState(thisChannelID, "Add_NewTimeCon")

        newHash = curTemp[3] + curTemp[2] * 288
        textTime = hashTime.hashBack(
            newHash)[0] + " " + hashTime.hashBack(newHash)[1]

        menus = ActionRow(
            dUse.acceptButton(pKey+"add_newTimeCon_OK"),
            dUse.anyButton(pKey+"add_newTimeCon_edit", "แก้ไขวัน/เวลา", "🕙")
        )
        m = await thisChannel.send(
            f"เวลาถูกไหม????",
            embed=Embed(
                title=curTemp[0],
                description=textTime, colour=Color.random()),
            components=[menus])
        dData.addMessageId(thisChannelID, m.id)

    # ? Edit Goes hereeeee

    elif idFlow == "Edi_SelSub":
        dData.setState(thisChannelID, "Edi_SelSub")
        pKey = dData.makeNewKey(thisChannelID) + ":"
        m = await thisChannel.send("**🔧 แก้ไขรายวิชา / เวลา +**\nกรุณาเลือกวิชาที่จะแก้ไข",
                                   components=[
                                       dUse.makeSelectSubject(
                                           thisChannelID, pKey+"edi_SelectSubject"),
                                       dUse.backToMenu(pKey)
                                   ])
        dData.addMessageId(thisChannelID, m.id)

    elif idFlow == "Edi_Sub":
        await delAllPrevMess(bot, thisChannelID)
        dData.setState(thisChannelID, "Edi_Sub")
        newTemp = dData.getTemp(thisChannelID)
        pKey = dData.makeNewKey(thisChannelID) + ":"
        thisEm = dUse.getEmbedAllTimeFromSubject(
            thisChannelID, newTemp[0], newTemp[1])
        m = await thisChannel.send(
            f"**ต้องการแก้ไขในส่วนไหน...**",
            embed=thisEm,
            components=[ActionRow(
                dUse.backToMenu(pKey),
                dUse.anyButton(pKey+"edit_sub_subj", "แก้ไขชื่อวิชา", "📕"),
                dUse.anyButton(pKey+"edit_sub_link", "แก้ไขลิ้ง", "🔗"),
                dUse.anyButton(pKey+"edit_sub_Time", "แก้ไขเวลา", "🕞"),
            )])
        dData.addMessageId(thisChannelID, m.id)

    elif idFlow == "Edi_ChaSub":
        await delAllPrevMess(bot, thisChannelID)
        dData.setState(thisChannelID, "Edi_ChaSub")
        await thisChannel.send(f":speech_balloon:กรุณาใส่ชื่อวิชาใหม่ จากวิชา {dData.getTempInd(thisChannelID, 0)} (ไม่เกิน 20 ตัวอักษร)")

    elif idFlow == "Edi_ChaLink":
        await delAllPrevMess(bot, thisChannelID)
        dData.setState(thisChannelID, "Edi_ChaLink")
        curSubject = dData.getTempInd(thisChannelID, 0)
        await thisChannel.send(
            f":closed_book: **วิชา `{curSubject}`**\n:speech_balloon: กรุณาใส่ลิ้งเรียนเลย\n*ขอแค่ลิ้งก็พอ*")

    elif idFlow == "Edi_ChaTime":
        await delAllPrevMess(bot, thisChannelID)
        dData.setState(thisChannelID, "Edi_ChaTime")
        curSubject = dData.getTempInd(thisChannelID, 0)
        allTimes = sData.getTimesfromSubject(thisChannelID, curSubject, False)
        pKey = dData.makeNewKey(thisChannelID) + ":"
        thisOptions = []
        for tim in allTimes:
            timeText = hashTime.hashBack(tim)
            thisOptions.append(SelectOption(
                label=f"{dUse.fromTerzTimeToStr(timeText)}", value=tim))

        m = await thisChannel.send(
            f"**กรุณาเลือกเวลาที่ต้องการแก้ไข...**",
            embed=dUse.getEmbedAllTimeFromSubject(
                thisChannelID, curSubject),
            components=[ActionRow(
                dUse.anyButton(pKey+"edit_chaTimSub",
                               "ย้อนกลับไปที่เมนูแก้ไข", "↩"),

            ), Select(
                placeholder="กรุณาเลือกเวลาที่จะแก้ไข",
                options=thisOptions,
                custom_id=pKey+"edit_chaTime"
            )])
        dData.addMessageId(thisChannelID, m.id)

    elif idFlow == "Edi_ChaTimeDay":
        await delAllPrevMess(bot, thisChannelID)
        dData.setState(thisChannelID, "Edi_ChaTimeDay")
        pKey = dData.makeNewKey(thisChannelID) + ":"
        dayInThai = ["อาทิตย์", "จันทร์", "อังคาร",
                     "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์"]
        fromDay = hashTime.hashBack(
            dData.getTempInd(thisChannelID, 2))[0]
        m = await thisChannel.send(
            f":calendar_spiral:**กรุณาเลือกวันที่จะเปลี่ยนจาก`{fromDay}`**:calendar_spiral:",
            components=[ActionRow(
                dUse.anyButton(pKey+"edi_chaTimeDay_0",
                               "วัน"+dayInThai[0], "🕒"),
                dUse.anyButton(pKey+"edi_chaTimeDay_1",
                               "วัน"+dayInThai[1], "🕒"),
                dUse.anyButton(pKey+"edi_chaTimeDay_2", "วัน"+dayInThai[2], "🕒")),
                ActionRow(
                dUse.anyButton(pKey+"edi_chaTimeDay_3",
                               "วัน"+dayInThai[3], "🕒"),
                dUse.anyButton(pKey+"edi_chaTimeDay_4",
                               "วัน"+dayInThai[4], "🕒"),
                dUse.anyButton(pKey+"edi_chaTimeDay_5",
                               "วัน"+dayInThai[5], "🕒"),
                dUse.anyButton(pKey+"edi_chaTimeDay_6",
                               "วัน"+dayInThai[6], "🕒"),
            )])
        dData.addMessageId(thisChannelID, m.id)

    elif idFlow == "Edi_ChaTimeTime":
        await delAllPrevMess(bot, thisChannelID)

        subJ = dData.getTempInd(thisChannelID, 0)
        fromTime = hashTime.hashBack(dData.getTempInd(thisChannelID, 2))
        dData.setState(thisChannelID, "Edi_ChaTimeTime")
        dayInThai = ["อาทิตย์", "จันทร์", "อังคาร",
                     "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์"]
        newDay = dayInThai[dData.getTempInd(thisChannelID, 3)]

        await thisChannel.send(
            f":clock3:วิชา `{subJ}`...\nจากเรียนใน `{dUse.fromTerzTimeToStr(fromTime)}`\nเปลี่ยนเป็น `วัน{newDay}` เวลา...?\n" +
            "* - ใส่เป็นเวลา `xx:xx` มาที่แชทนี้เลย*\n" +
            "* - เวลาจะรับได้แค่เวลาที่หารด้วย 5 ลงตัว เช่น 0:00 0:05 0:10 เป็นต้น*")

    elif idFlow == "Rem_SelSub":
        dData.setState(thisChannelID, "Rem_SelSub")
        await delAllPrevMess(bot, thisChannelID)
        pKey = dData.makeNewKey(thisChannelID) + ":"
        m = await thisChannel.send("**✂ ลบรายวิชา / เวลา +**\nกรุณาเลือกวิชาที่จะแก้ไขโดยการลบ",
                                   components=[
                                       dUse.makeSelectSubject(
                                           thisChannelID, pKey+"rem_SelectSubject",
                                           [("ลบทุกวิชา!!!!", "!!RRREEEEMMMMOOvEEEEEEALL!!!", "💥")]),
                                       dUse.backToMenu(pKey)
                                   ])
        dData.addMessageId(thisChannelID, m.id)

    elif idFlow == "Rem_AllSubCon":
        dData.setState(thisChannelID, "Rem_AllSubCon")
        await delAllPrevMess(bot, thisChannelID)
        pKey = dData.makeNewKey(thisChannelID) + ":"
        m = await thisChannel.send("**💥💥คุณกำลังจะลบทุก ๆ วิชา💥💥**\nหากลบแล้ว จะไม่สามารถกู้คืนได้ แน่ใจแล้วหรือไม่",
                                   components=[ActionRow(
                                       Button(
                                           label="แน่ใจแล้วที่จะลบ!!!",
                                           custom_id=pKey + "rem_allSubCon_Remove",
                                           style=ButtonStyle.red,
                                           emoji="💥"),
                                       dUse.anyButton(pKey + "rem_allSubCon_cancel",
                                                      "ยังก่อน ยังไม่ลบ", "↩")
                                   )])
        dData.addMessageId(thisChannelID, m.id)

    elif idFlow == "Rem_Sub":
        await delAllPrevMess(bot, thisChannelID)
        dData.setState(thisChannelID, "Rem_Sub")
        newTemp = dData.getTemp(thisChannelID)
        pKey = dData.makeNewKey(thisChannelID) + ":"
        thisEm = dUse.getEmbedAllTimeFromSubject(
            thisChannelID, newTemp[0], newTemp[1])
        m = await thisChannel.send(
            f"**ต้องการลบในส่วนไหน...**",
            embed=thisEm,
            components=[ActionRow(
                dUse.anyButton(pKey+"rem_sub_back", "ย้อนกลับ", "↩"),
                dUse.anyButton(pKey+"rem_sub_subj", "ลบวิชา", "📕"),
                dUse.anyButton(pKey+"rem_sub_Time", "ลบเวลา", "🕞"),
            )])
        dData.addMessageId(thisChannelID, m.id)

    elif idFlow == "Rem_SubCon":
        dData.setState(thisChannelID, "Rem_SubCon")
        await delAllPrevMess(bot, thisChannelID)
        pKey = dData.makeNewKey(thisChannelID) + ":"
        thisSub = dData.getTempInd(thisChannelID, 0)
        m = await thisChannel.send(f"**💥คุณกำลังจะลบวิชา `{thisSub}`💥**\nหากลบแล้ว จะไม่สามารถกู้คืนได้ แน่ใจแล้วหรือไม่",
                                   components=[ActionRow(Button(
                                       label="ลบ!!",
                                       custom_id=pKey + "rem_subCon_Remove",
                                       style=ButtonStyle.red,
                                       emoji="💥"),
                                       dUse.anyButton(pKey + "rem_subCon_cancel",
                                                      "ยังก่อน ยังไม่ลบ", "↩")
                                   )
                                   ])
        dData.addMessageId(thisChannelID, m.id)

    elif idFlow == "Rem_SelTimeSub":
        await delAllPrevMess(bot, thisChannelID)
        dData.setState(thisChannelID, "Rem_SelTimeSub")
        curSubject = dData.getTempInd(thisChannelID, 0)
        allTimes = sData.getTimesfromSubject(thisChannelID, curSubject, False)
        pKey = dData.makeNewKey(thisChannelID) + ":"
        thisOptions = []
        for tim in allTimes:
            timeText = hashTime.hashBack(tim)
            thisOptions.append(SelectOption(
                label=f"{dUse.fromTerzTimeToStr(timeText)}", value=tim))

        m = await thisChannel.send(
            f"**กรุณาเลือกเวลาที่ต้องการลบ...**\n*หากเลือกแล้ว จะทำการ**ลบทันที!!!!***",
            embed=dUse.getEmbedAllTimeFromSubject(
                thisChannelID, curSubject),
            components=[ActionRow(
                dUse.anyButton(pKey+"rem_selTimeSub_back",
                               "ย้อนกลับไปที่เมนูวิชา", "↩"),

            ), Select(
                placeholder="กรุณาเลือกเวลาที่จะลบ",
                options=thisOptions,
                custom_id=pKey+"rem_selTimeSub_rem"
            )])
        dData.addMessageId(thisChannelID, m.id)

    elif idFlow == "tog_vaca":
        isVaca = dlcc
        dData.setState(thisChannelID, "Tog_vaca")
        pKey = dData.makeNewKey(thisChannelID) + ":"

        if isVaca:
            m = await thisChannel.send("🎉เย่ ๆ ไม่มีเรียน\nแล้วหยุดกี่วัน",
                                       components=[
                                           dUse.backToMenu(pKey),
                                           Select(
                                               placeholder="กรุณาเลือกจำนวนวัน",
                                               options=[
                                                   SelectOption(
                                                       label="1 วัน", value="1"),
                                                   SelectOption(
                                                       label="2 วัน", value="2"),
                                                   SelectOption(
                                                       label="3 วัน", value="3"),
                                                   SelectOption(
                                                       label="4 วัน", value="4"),
                                                   SelectOption(
                                                       label="5 วัน", value="5"),
                                                   SelectOption(
                                                       label="6 วัน", value="6"),
                                                   SelectOption(
                                                       label="1 สัปดาห์", value="7"),
                                                   SelectOption(
                                                       label="2 สัปดาห์", value="14"),
                                                   SelectOption(
                                                       label="3 สัปดาห์", value="21"),
                                                   SelectOption(
                                                       label="1 เดือน", value="30"),
                                                   SelectOption(
                                                       label="2 เดือน", value="60"),
                                                   SelectOption(
                                                       label="3 เดือน", value="90"),
                                               ],
                                               custom_id=pKey+"tog_vaca"
                                           )
                                       ])
            dData.addMessageId(thisChannelID, m.id)
        else:
            await thisChannel.send("💧กลับมาเรียนเหมือนเดิม")
            dData.setVacation(thisChannelID, 0)
            await callFlow("backToIdle", bot, thisChannelID)

    elif idFlow == "tog_noti":
        newMode = dData.toggleNotiMode(thisChannelID)
        expP = newMode == "Subject" and "แบบรายวิชา" or "วัน"
        await thisChannel.send(f"💬เปลี่ยนจากการแจ้งเตือนเป็น `{expP}`")
        await callFlow("backToIdle", bot, thisChannelID)
