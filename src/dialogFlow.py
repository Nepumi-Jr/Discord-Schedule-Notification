from discord.colour import Color
from discord.embeds import Embed
from discord_components import Select, Button, DiscordComponents, interaction, ActionRow, SelectOption
from discord_components.component import ButtonStyle

from src import discordData as dData
from src.backend import handle as sData
from src.backend import hashTime
from src import cmdUtil as util


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
            Button(
                label="วุ้ฮู้วววว วันนี้ไม่มีเรียน",
                custom_id="toggleNoToday",
                style=ButtonStyle.gray,
                emoji="🎉",
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
                label="ตรวจสอบเวอร์ชั่น",
                custom_id="checkVersion",
                style=ButtonStyle.gray,
                emoji="⏫",
                disabled=True),
            Button(
                label="เริ่มต้นการทำงานใหม่",
                custom_id="FreloadButton",
                style=ButtonStyle.red,
                emoji="⚠"),
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
        lastMessage = await getMessage(bot, thisChannelID, dData.getMessID(thisChannelID))
        await lastMessage.delete()
    except:
        pass


async def menuCmdCommand(chan):
    return await chan.send(":clock1:**ยินดีต้อนรับสู่การใช้งาน บอทขอลิงก์(ห้อง)เรียน**:clock1:\n \\* สามารถใช้ปุ่มด้านล่างนี้ในการควบคุมต่าง ๆ\n*แนะนำ : ไม่ควรใช้ห้องแชทนี้ในการสนทนาปกติ*",
                           components=getMenuComponents())


async def callFlow(idFlow, bot, thisChannelID, dlcc=None):
    thisChannel = bot.get_channel(thisChannelID)
    if idFlow == "callSchedule":
        thisMes = await menuCmdCommand(thisChannel)
        if dData.isExistID(thisChannelID):
            await doDeleteLastCMDMessage(bot, thisChannelID)
            dData.setMessID(thisChannelID, thisMes.id)
        else:
            dData.createNewID(thisChannelID, thisMes.id)
    elif idFlow == "deleteChan":
        if dData.isExistID(thisChannelID):
            await doDeleteLastCMDMessage(bot, thisChannelID)
            dData.removeID(thisChannelID)
            await thisChannel.send(":boom:**ลบแชลเนลเรียบร้อย**:boom:\nหวังว่าจะได้ให้บริการอีกครั้ง *(ซึม...)*")
        else:
            await thisChannel.send("เ ป็ น ไ ป ไ ม่ ไ ด้")
    elif idFlow == "justReload":
        await doDeleteLastCMDMessage(bot, thisChannelID)
        thisMes = await menuCmdCommand(thisChannel)
        dData.setMessID(thisChannelID, thisMes.id)
    elif idFlow == "forceReload":
        await thisChannel.send("-"*50)
        dData.setState(thisChannelID, "idle")
        dData.setTemp(thisChannelID, [])
        await thisChannel.send("🔁เริ่มต้นระบบใหม่🔁")
        await doDeleteLastCMDMessage(bot, thisChannelID)
        thisMes = await menuCmdCommand(thisChannel)
        dData.setMessID(thisChannelID, thisMes.id)
    elif idFlow == "backToIdle":
        dData.setState(thisChannelID, "idle")
        dData.setTemp(thisChannelID, [])
        pKey = util.genRandomKey()
        dData.setStateKey(thisChannelID, pKey)
        await doDeleteLastCMDMessage(bot, thisChannelID)
        thisMes = await menuCmdCommand(thisChannel)
        dData.setMessID(thisChannelID, thisMes.id)

    # ? ADDD

    elif idFlow == "Add_SelSub":
        dData.setState(thisChannelID, "Add_SelSub")
        pKey = util.genRandomKey()
        dData.setStateKey(thisChannelID, pKey)
        pKey += ":"
        subjects = sData.getallSubjects(thisChannelID)
        subOption = []
        for s in subjects:
            subOption.append(SelectOption(label=s, value=s))
        subOption.append(SelectOption(label="+ เพิ่มวิชาใหม่",
                         value="!!TheNewOneeeeeeeeeeeeeee!!",
                         emoji="➕"))
        await thisChannel.send("**+ เพิ่มรายวิชา / เวลา +**\nกรุณาเลือกวิชาที่จะเพิ่มเวลาหรือเพิ่มวิชา",
                               components=[
                                   Select(
                                       placeholder="กรุณาเลือกวิชา",
                                       options=subOption,
                                       custom_id=pKey+"add_SelectSubject"
                                   )
                               ])
    elif idFlow == "Add_Sub":
        dData.setState(thisChannelID, "Add_Sub")
        await thisChannel.send(":speech_balloon:กรุณาใส่ชื่อวิชาที่จะต้องการเพิ่ม (ไม่เกิน 20 ตัวอักษร)\n*ส่งมาในแชทนี้เลย*")

    elif idFlow == "Add_Sub2":
        dData.setState(thisChannelID, "Add_Sub2")
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
        pKey = dData.getStateKey(thisChannelID) + ":"
        dData.setState(thisChannelID, "Add_SubCon")

        menus = ActionRow(
            Button(
                label="ตกลง",
                custom_id=pKey+"add_sub_OK",
                style=ButtonStyle.green,
                emoji="✅"),
            Button(
                label="แก้ไขชื่อวิชา",
                custom_id=pKey+"add_sub_editSub",
                style=ButtonStyle.gray,
                emoji="📕"),
            Button(
                label="แก้ไขลิ้ง",
                custom_id=pKey+"add_sub_editLink",
                style=ButtonStyle.gray,
                emoji="🔗"),
        )
        try:
            await thisChannel.send(
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
            await thisChannel.send(
                f"**กรอกข้อมูลวิชาสำเร็จ**\nหน้าตาจะออกมาเป็นแบบนี้",
                embed=Embed(
                    title=newTemp[0],
                    description=newTemp[1], colour=Color.random()),
                components=[menus])

    elif idFlow == "Add_AllTime":
        dData.setState(thisChannelID, "Add_AllTime")
        newTemp = dData.getTemp(thisChannelID)
        pKey = dData.getStateKey(thisChannelID) + ":"
        thisEm = Embed(
            title=newTemp[0], description=newTemp[1], colour=Color.random())
        timeDatas = sData.getTimesfromSubject(thisChannelID, newTemp[0])
        for t in timeDatas:
            print(t)
            thisEm.add_field(name=t, value="Ayaya", inline=True)
        await thisChannel.send(
            f"**ข้อมูลวิชาเวลา...**",
            embed=thisEm,
            components=[ActionRow(
                Button(
                        label="สำเร็จ",
                        custom_id=pKey+"add_time_OK",
                        style=ButtonStyle.green,
                        emoji="✅"),
                Button(
                    label="เพิ่มเวลาเรียน",
                    custom_id=pKey+"add_time_add",
                    style=ButtonStyle.blue,
                    emoji="🕒"),
            )])

    elif idFlow == "Add_NewDay":
        dData.setState(thisChannelID, "Add_NewDay")
        pKey = dData.getStateKey(thisChannelID) + ":"
        await thisChannel.send(
            f":calendar_spiral:**กรุณาเลือกวันที่เรียน**:calendar_spiral:",
            components=[ActionRow(
                Button(
                        label="วันอาทิตย์",
                        custom_id=pKey+"add_NewDay_0",
                        style=ButtonStyle.gray),
                Button(
                    label="วันจันทร์",
                    custom_id=pKey+"add_NewDay_1",
                    style=ButtonStyle.gray),
                Button(
                    label="วันอังคาร",
                    custom_id=pKey+"add_NewDay_2",
                    style=ButtonStyle.gray)), ActionRow(
                Button(
                    label="วันพุธ",
                    custom_id=pKey+"add_NewDay_3",
                    style=ButtonStyle.gray),
                Button(
                    label="วันพฤหัสบดี",
                    custom_id=pKey+"add_NewDay_4",
                    style=ButtonStyle.gray),
                Button(
                    label="วันศุกร์",
                    custom_id=pKey+"add_NewDay_5",
                    style=ButtonStyle.gray),
                Button(
                    label="วันเสาร์",
                    custom_id=pKey+"add_NewDay_6",
                    style=ButtonStyle.gray),
            )])

    elif idFlow == "Add_NewTime":
        dData.setTempInd(thisChannelID, 2, dlcc)
        ttemp = dData.getTemp(thisChannelID)
        dData.setState(thisChannelID, "Add_NewTime")
        dayInThai = ["อาทิตย์", "จันทร์", "อังคาร",
                     "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์"]

        await thisChannel.send(
            f":clock3:วิชา {ttemp[0]} ในทุก ๆ วัน{dayInThai[dlcc]} ตอนกี่โมง??\n" +
            "* - ใส่เป็นเวลา `xx:xx` มาที่แชทนี้เลย*\n" +
            "* - พยายามให้ตั้งก่อนเวลาเรียนประมาณ 5-10 นาที...*\n" +
            "* - เวลาจะรับได้แค่เวลาที่หารด้วย 5 ลงตัว เช่น 0:00 0:05 0:10 เป็นต้น*")

    elif idFlow == "Add_NewTimeCon":
        dData.setTempInd(thisChannelID, 3, dlcc[0]*12 + dlcc[1]//5)
        curTemp = dData.getTemp(thisChannelID)
        pKey = dData.getStateKey(thisChannelID) + ":"
        dData.setState(thisChannelID, "Add_NewTimeCon")

        newHash = curTemp[3] + curTemp[2] * 288

        menus = ActionRow(
            Button(
                label="ตกลง",
                custom_id=pKey+"add_newTimeCon_OK",
                style=ButtonStyle.green,
                emoji="✅"),
            Button(
                label="แก้ไขวัน/เวลา",
                custom_id=pKey+"add_newTimeCon_edit",
                style=ButtonStyle.gray,
                emoji="🕙")
        )
        await thisChannel.send(
            f"เวลาถูกไหม????",
            embed=Embed(
                title=curTemp[0],
                description=hashTime.hashBack(newHash), colour=Color.random()),
            components=[menus])
