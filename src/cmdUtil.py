def isAdmin(idUser) -> bool:
    pass
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


def regisAdmin(idUser, passText: str) -> int:
    pass
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
