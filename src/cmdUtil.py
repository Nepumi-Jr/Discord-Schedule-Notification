def isAdmin(idUser) -> bool:
    # TODO : คำสั่งนี้เป็นคำสั่งสำหรับเช็คว่าคนนี้เป็น Admin หรือเปล่า
    # * จะให้อ่านไฟล์ที่ชื่อว่า AdminUsers.txt ที่อยู่นอกโฟลเดอร์ src
    # * โดยไฟล์จะมีลักษณะแบบนี้
    """
    143242345
    123222545
    993224234
    """

    # ? ตัวอย่าง isAdmin(123222545) -> True
    # ? ตัวอย่าง isAdmin(993224234) -> True
    # ? ตัวอย่าง isAdmin(142342345) -> False

    file_path = "../AdminUsers.txt"
    with open(file_path, 'r') as ID:
        while ID:
            line = ID.readline().strip()
            if idUser == line:
                return True
            if line == "":
                return False


def regisAdmin(idUser, passText: str) -> int:
    # TODO : คำสั่งนี้เป็นคำสั่งสำหรับการใส่ข้อมูลว่าคนนั้นเป็น admin
    # * จะให้อ่านไฟล์ที่ชื่อว่า AdminPassword.pass ที่อยู่นอกโฟลเดอร์ src
    # * โดยไฟล์จะมีลักษณะแบบนี้
    """
    Hello world
    123 cute cute
    """
    # * ถ้า `passText` ตรงกับบรรทัดใดบรรทัดหนึ่งใน AdminPassword.pass
    # * ก็ให้บรรจุ idUser ลงใน AdminUsers.txt และคืนค่า 1 ออกไป
    # ! (ถ้าทำได้) ในกรณีที่มี idUser อยู่ใน AdminUsers.txt อยู่แล้ว ไม่ต้องใส่ และคืนค่า 2 ออกไป
    # * หาก passText` ไม่ตรงกับบรรทัดไหนเลย ไม่ต้องบรรจุ และคืนค่า 0 ออกไป

    # ? ตัวอย่าง regisAdmin(123222545, "Hello world") -> 1 (บรรจุด้วย)
    # ? ตัวอย่าง regisAdmin(993224234, "Hello world") -> 1 (บรรจุด้วย)
    # ? ตัวอย่าง regisAdmin(123222545, "123 cute cute") -> 2 (ไม่บรรจุ)
    # ? ตัวอย่าง regisAdmin(142342345, "456 brbrbr") -> 0 (ไม่บรรจุ)


    # * เชคว่า passText ตรงกับ AdminPassword หรือไม่
    file_path = "../AdminPassword.pass"
    with open(file_path, 'r') as ID:
        while ID:
            line = ID.readline().strip()
            if str(passText) == str(line):
                passTextBool = True
                break
            if line == "":
                passTextBool = False


    # * เงื่อนไขการตรวจสอบ
    if (isAdmin(idUser) and passTextBool):
        return 2
    elif passTextBool:
        file_path = "../AdminUsers.txt"
        f = open(file_path, "a")
        f.write("\n"+idUser)
        f.close()
        return 1
    else:
        return 0
            

def main():
    a = regisAdmin("1234956","Hello world")
    print(a)


if __name__ == "__main__":
    main()
