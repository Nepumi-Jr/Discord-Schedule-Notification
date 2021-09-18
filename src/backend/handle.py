# from src.backend.hashTime import *
from hashTime import *
import pprint

userData = {}
timeTable = [dict() for i in range(2020)]


def insertOfUser(idUser, timeSet: int, subject: str, at: str):
    global userData, timeTable
    hashedTime = hash(timeSet)
    if idUser not in userData:
        userData[idUser] = {
            "isAdmin": False,
            "timeOffset": 0,
            "lang": "TH",
            "timeData": {
                hashedTime: (subject, at)
            }
        }
    else:
        userData[idUser]["timeData"][hashedTime] = (subject, at)

    timeTable[hashedTime][idUser] = ((subject, at))


def delByTime(idUser, atTime: int):
    global userData, timeTable
    hashedTime = hash(atTime)
    if idUser in userData and hashedTime in userData[idUser]["timeData"]:
        del userData[idUser]["timeData"][hashedTime]
    del timeTable[hashedTime][idUser]


def delAllTime(idUser):
    global userData, timeTable
    if idUser in userData:
        for eachTimeData in userData[idUser]["TimeData"]:
            del timeTable[eachTimeData][idUser]

        del userData[idUser]


def getStrUserSubject(idUser) -> str:
    global userData, timeTable
    result = f"{'='*15}User : {idUser} {'='*15}\n"
    if idUser in userData:
        result += f" - IsAdmin : {userData[idUser]['isAdmin']}\n"
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
    hashedTime = hash(time)
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
    hashedTime = hash(time)
    result = []
    if timeTable[hashedTime]:
        for userId in timeTable[hashedTime]:
            result.append((userId, timeTable[hashedTime][userId]))
    else:
        return None
    return result


def getUserSubject(idUser):
    global userData, timeTable
    if idUser in userData:
        return userData[idUser]
    else:
        return None


if __name__ == "__main__":
    printUserSubject(69)
    printTimeSubject(1)
    insertOfUser(69, 1, "DMath", "googoo.com")
    insertOfUser(72, 1, "DataStruct", "x.com")
    insertOfUser(63, 1, "Analog", "ty.com")
    printUserSubject(69)
    printTimeSubject(1)
