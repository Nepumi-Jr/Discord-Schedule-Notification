from src.backend.hashTime import *
# from hashTime import *
import pprint
import yaml
from src import cmdUtil

userData = dict()
timeTable = [dict() for i in range(2020)]


def saveData():
    global userData, timeTable
    with open("sUserData.yml", "w") as f:
        yaml.dump(userData, f)

    with open("sTimeTable.yml", "w") as f:
        yaml.dump(timeTable, f)


def loadData():
    global userData, timeTable
    cmdUtil.fileExist("sUserData.yml")
    cmdUtil.fileExist("sTimeTable.yml")
    with open("sUserData.yml", "r") as f:
        userData = yaml.load(f, Loader=yaml.FullLoader)

    with open("sTimeTable.yml", "r") as f:
        timeTable = yaml.load(f, Loader=yaml.FullLoader)

    if userData == None:
        userData = dict()

    if timeTable == None:
        timeTable = [dict() for i in range(2020)]


def insertOfUser(idUser, timeSet: int, subject: str, at: str, saveD=True):
    global userData, timeTable
    hashedTime = timeSet
    if idUser not in userData:
        userData[idUser] = {
            "timeData": {
                hashedTime: (subject, at)
            }
        }
    else:
        userData[idUser]["timeData"][hashedTime] = (subject, at)

    timeTable[hashedTime][idUser] = ((subject, at))

    if saveD:
        saveData()


def delByTime(idUser, atTime: int, saveD=True):
    global userData, timeTable
    hashedTime = atTime
    if idUser in userData and hashedTime in userData[idUser]["timeData"]:
        del userData[idUser]["timeData"][hashedTime]
    del timeTable[hashedTime][idUser]

    if saveD:
        saveData()


def delAllTime(idUser, saveD=True):
    global userData, timeTable
    if idUser in userData:
        for eachTimeData in userData[idUser]["TimeData"]:
            del timeTable[eachTimeData][idUser]

        del userData[idUser]

    if saveD:
        saveData()


def getStrUserSubject(idUser) -> str:
    global userData, timeTable
    result = f"{'='*15}User : {idUser} {'='*15}\n"
    if idUser in userData:
        result += f" - timeOff : {userData[idUser]['timeOffset']}\n"
        result += f" - langggg : {userData[idUser]['lang']}\n"
        result += f" - timeDat...\n"
        for e in userData[idUser]["timeData"]:
            result += f"   * [{e}] {userData[idUser]['timeData'][e]}\n"
    else:
        result += " - no Data -\n"
    return result


def printUserSubject(idUser):
    print(getStrUserSubject(idUser))


def getStrTimeSubject(time: int) -> str:
    global userData, timeTable
    hashedTime = time
    result = f"{'='*15}Time : {time}({hashedTime}) {'='*15}\n"
    if timeTable[hashedTime]:
        for e in timeTable[hashedTime]:
            result += f" - {e} => {timeTable[hashedTime][e]}\n"
    else:
        result += " - no Data -\n"
    return result


def printTimeSubject(time: int):
    print(getStrTimeSubject(time))


def getTimeSubject(time: int):
    global userData, timeTable
    hashedTime = time
    result = []
    if timeTable[hashedTime]:
        for userId in timeTable[hashedTime]:
            result.append((userId, timeTable[hashedTime][userId]))
    else:
        return None
    return result


def getfullUserData(idUser):
    global userData, timeTable
    if idUser in userData:
        return userData[idUser]
    else:
        return None


def getallSubjects(idUser):
    global userData
    if idUser in userData:
        tempp = set()
        for tim in userData[idUser]["timeData"]:
            tempp.add(userData[idUser]["timeData"][tim][0])
        return list(tempp)
    else:
        return []


def getLinkfromSubject(idUser, subject: str):
    global userData
    if idUser in userData:
        res = []
        for tim in userData[idUser]["timeData"]:
            if userData[idUser]["timeData"][tim][0] == subject:
                return userData[idUser]["timeData"][tim][1]
        return ""
    else:
        return []


def getTimesfromSubject(idUser, subject: str, isHashBack=True):
    global userData
    if idUser in userData:
        res = []
        for tim in userData[idUser]["timeData"]:
            if userData[idUser]["timeData"][tim][0] == subject:
                if isHashBack:
                    res.append(hashBack(tim))
                else:
                    res.append(tim)
        return res
    else:
        return []


def getDesFromSubject(idUser, subject: str):
    global userData
    if idUser in userData:
        res = "???"
        for tim in userData[idUser]["timeData"]:
            if userData[idUser]["timeData"][tim][0] == subject:
                return userData[idUser]["timeData"][tim][1]
        return res
    else:
        return "???"


def delSubject(idUser, subj, saveD=True):

    thatTime = getTimesfromSubject(subj)

    for tim in thatTime:
        delByTime(idUser, tim, False)

    if saveD:
        saveData()


def changeSubject(idUser, fromSubject, toSubject):

    global userData
    if idUser in userData:
        thisData = []
        for tim in userData[idUser]["timeData"]:
            if userData[idUser]["timeData"][tim][0] == fromSubject:
                thisData.append(
                    (fromSubject, userData[idUser]["timeData"][tim][1], tim))

        for d in thisData:
            delByTime(idUser, d[2], False)
            insertOfUser(idUser, d[2], toSubject, d[1], False)

        saveData()


def changeLink(idUser, subject, toLink):

    global userData
    if idUser in userData:
        thisData = []
        for tim in userData[idUser]["timeData"]:
            if userData[idUser]["timeData"][tim][0] == subject:
                thisData.append(
                    (subject, userData[idUser]["timeData"][tim][1], tim))

        for d in thisData:
            delByTime(idUser, d[2], False)
            insertOfUser(idUser, d[2], subject, toLink, False)
        saveData()


def changeTime(idUser, fromTime, toTime):
    global userData
    if idUser in userData and fromTime in userData[idUser]["timeData"]:
        thisData = userData[idUser]["timeData"][fromTime]
        delByTime(idUser, fromTime, False)
        insertOfUser(idUser, toTime, thisData[0], thisData[1], False)
        saveData()


def isExistId(idUser):
    if idUser in userData:
        return len(userData[idUser]["timeData"]) > 0
    else:
        return False


if __name__ == "__main__":
    printUserSubject(69)
    printTimeSubject(1)
    insertOfUser(69, 1, "DMath", "googoo.com")
    insertOfUser(72, 1, "DataStruct", "x.com")
    insertOfUser(63, 1, "Analog", "ty.com")
    printUserSubject(69)
    printTimeSubject(1)
