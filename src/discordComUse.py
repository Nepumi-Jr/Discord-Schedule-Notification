from discord_components import Select, Button, DiscordComponents, interaction, ActionRow, SelectOption
from discord_components.component import ButtonStyle
from discord.colour import Color
from discord.embeds import Embed

from src.backend import handle as sData


def getMenuComponents(thisChannelID):
    editDelDisable = not sData.isExistId(thisChannelID)
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
                disabled=editDelDisable),
            Button(
                label="ลบรายวิชา/เวลา",
                custom_id="delButton",
                style=ButtonStyle.red,
                emoji="❌",
                disabled=editDelDisable),
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


def getEmbedAllTimeFromSubject(thisChannelID, subject, des=None):

    if not des:
        des = sData.getDesFromSubject(thisChannelID, subject)

    thisEm = Embed(
        title=subject, description=des, colour=Color.random())
    timeDatas = sData.getTimesfromSubject(thisChannelID, subject)
    for t in timeDatas:
        thisEm.add_field(name=t[0], value=t[1], inline=True)

    return thisEm


def anyButton(customId, llabel, eemoji=""):
    return Button(
        label=llabel,
        custom_id=customId,
        style=ButtonStyle.gray,
        emoji=eemoji)


def acceptButton(customId):
    return Button(
        label="ตกลง",
        custom_id=customId,
        style=ButtonStyle.green,
        emoji="✅")


def backToMenu(pKey):
    return Button(
        label="กลับสู่เมนู",
        custom_id=pKey + "backToMenu",
        style=ButtonStyle.gray,
        emoji="↩")


def makeSelectSubject(thisChannelID, customId, makeNewSubject):
    subOption = []
    subjects = sData.getallSubjects(thisChannelID)
    for s in subjects:
        subOption.append(SelectOption(label=s, value=s))
    if makeNewSubject:
        subOption.append(SelectOption(label="+ เพิ่มวิชาใหม่",
                                      value="!!TheNewOneeeeeeeeeeeeeee!!",
                                      emoji="➕"))
    return Select(
        placeholder="กรุณาเลือกวิชา",
        options=subOption,
        custom_id=customId
    )


def fromTerzTimeToStr(timeTerz):
    return f"{timeTerz[0]} เวลา {timeTerz[1]}"
