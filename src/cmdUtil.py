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
    content = content.replace(":"," ").replace("."," ")
    word = content.split(" ")
    time = []
    for text in word:
        if text.isdigit():
            time.append(int(text))
    if not(len(time) == 2):
        return ()
    if (time[0] >= 0 and time[0] <= 23) and (time[1] >= 0 and time[1] <= 59):
        return tuple(time)
    return ()

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
    print(timeDetection("0 61 นาที"))
    print(timeDetection("23:59 นาที"))

if __name__ == "__main__":
    main()
