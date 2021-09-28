from os import path

srcPath = ""

if __name__ == "__main__":
    srcPath = "../"


def fileExist(thisPath):
    if not path.exists(thisPath):
        with open(thisPath, "w") as f:
            f.write("")


def isAdmin(idUser) -> bool:
    file_path = srcPath+"AdminUsers.txt"
    fileExist(file_path)
    with open(file_path, 'r') as ID:
        while ID:
            line = ID.readline().strip()
            if idUser == line:
                return True
            if line == "":
                return False


def regisAdmin(idUser, passText: str) -> int:
    file_path = srcPath+"AdminPassword.pass"
    fileExist(file_path)
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
        file_path = srcPath+"AdminUsers.txt"
        f = open(file_path, "a")
        f.write("\n"+idUser)
        f.close()
        return 1
    else:
        return 0


def isUseChannel(idChannel: int) -> bool:
    file_path = srcPath+"useChannel.txt"
    fileExist(file_path)

    with open(file_path, 'r') as ID:
        data = ID.read().strip().split("\n")

    # BSearch
    l = 0
    r = len(data)-1
    while l <= r:
        mid = (l+r)//2
        if data[mid].strip() == str(idChannel):
            return True
        elif str(idChannel) < data[mid].strip():
            r = mid - 1
        else:
            l = mid + 1

    return False


def regisChannel(idChannel: int) -> int:
    file_path = srcPath+"useChannel.txt"
    fileExist(file_path)

    # * เงื่อนไขการตรวจสอบ
    if (isUseChannel(idChannel)):
        return 2
    else:
        with open(file_path, 'r') as ID:
            data = ID.read().strip().split("\n")
        data.append(str(idChannel))
        data = sorted(data)
        with open(file_path, 'w') as ID:
            ID.write("\n".join(data).strip())
        return 1


def timeDetection(content: str) -> tuple:
    # TODO : ฟังก์ชั่นนี้จะทำการอ่าน string content และให้ส่งค่าออกมาเป็นเวลา
    # * แนะนำให้เขียนเป็นฟังก์ชั่นในการหาตัวเลขจำนวนเต็มสองตัวใน string นี้ แล้วค่อยเช็คว่ามันเป็นเวลาที่ถูกไหม
    # ? เงื่อนไขที่เป็นเวลาคือ ชั่วโมง จะอยู่ในช่วง [0,23] และ นาที จะอยู่ในช่วง [0,59]
    # ? หากเป็นเวลา ให้คืนค่าเป็น Tuple สองตัว นั้นคือชม. และนาที
    # ? หากไม่ใช่เวลา ให้คืนค่าเป็น Tuple ว่างเปล่า

    # * ตัวอย่าง
    "12 : 45"
    # * Return -> (12,45)

    "13.57 น."
    # * Return -> (13,57)

    "0 โมง 23 นาที"
    # * Return -> (0,23)

    "ตั้งตอน 11 นาฬิกา 22 นาที"
    # * Return -> (11,22)

    "23 โมง"
    # ! Return -> ()

    "1232"
    # ! Return -> ()

    "24.12"
    # ! Return -> ()

    "งึกๆงักๆ มันเป็นงึกๆงักๆ"
    # ! Return -> ()
    pass


def main():
    print(isUseChannel(123))
    print(regisChannel(123))
    print(isUseChannel(123))
    print(isUseChannel(456))
    print(regisChannel(456))
    print(regisChannel(456))
    print(regisChannel(12))
    print(regisChannel(1342))
    print(isUseChannel(12))
    print(isUseChannel(1342))
    print(isUseChannel(23))


if __name__ == "__main__":
    main()
