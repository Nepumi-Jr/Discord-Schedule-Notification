from discord_components import Select, Button, DiscordComponents, interaction, ActionRow, SelectOption
from discord_components.component import ButtonStyle


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
