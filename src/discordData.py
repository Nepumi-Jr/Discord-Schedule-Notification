import yaml
from src import cmdUtil

thisData = dict()
serverData = dict()
DEFAULT_DATA = {
    "modeNofi": "Subject",
    "state": "idle",
    "stateKey": "AAAAA",
    "CMDmessID": 69,
    "notiMessId": -1,
    "temp": [],
    "prevMessage": [],
    "vacationDays": 0,
    "dynamicDay": -1,
    "dynamicTime": -1,
    "missingCrt": 0,
}

DEFAULT_SERVER_DATA = {
    "dayOfWeek": -1,
    "timeOfWeek": -1,
    "dmy": [],
    "chanReload": [],
    "timeReload": []
}


def saveData():
    global thisData, serverData
    with open("data/disData.yml", "w") as f:
        yaml.dump(thisData, f)


def saveServerData():
    global thisData, serverData
    with open("data/serverData.yml", "w") as f:
        yaml.dump(serverData, f)


def validData():

    for e in thisData:
        for f in DEFAULT_DATA:
            if f not in thisData[e]:
                thisData[e][f] = DEFAULT_DATA[f]

    for f in DEFAULT_SERVER_DATA:
        if f not in serverData:
            serverData[f] = DEFAULT_SERVER_DATA[f]

    saveData()
    saveServerData()


def loadData():
    global thisData, serverData
    cmdUtil.fileExist("data/disData.yml")
    cmdUtil.fileExist("data/serverData.yml")
    with open("data/disData.yml", "r") as f:
        thisData = yaml.load(f, Loader=yaml.FullLoader)

    with open("data/serverData.yml", "r") as f:
        serverData = yaml.load(f, Loader=yaml.FullLoader)

    if thisData == None:
        thisData = dict()
    if serverData == None:
        serverData = dict()

    validData()


def isExistID(thisId: int) -> bool:
    if thisData:
        return thisId in thisData
    else:
        return False


def setMessID(thisId: int, messId: int):
    if isExistID(thisId):
        thisData[thisId]["CMDmessID"] = messId
        saveData()


def getMessID(thisId: int):
    if isExistID(thisId):
        return thisData[thisId]["CMDmessID"]
    return 0


def setNotiMessID(thisId: int, messId: int):
    if isExistID(thisId):
        thisData[thisId]["notiMessId"] = messId
        saveData()


def getNotiMessID(thisId: int):
    if isExistID(thisId):
        return thisData[thisId]["notiMessId"]
    return 0


def getState(thisId: int) -> str:
    if isExistID(thisId):
        return thisData[thisId]["state"]
    return 0


def setState(thisId: int, stat: str):
    if isExistID(thisId):
        thisData[thisId]["state"] = stat
        saveData()


def getTemp(thisId: int) -> str:
    if isExistID(thisId):
        return thisData[thisId]["temp"].copy()
    return 0


def getTempInd(thisId: int, ind: int) -> str:
    if isExistID(thisId):
        bData = thisData[thisId]["temp"]
        if ind < len(bData):
            return bData[ind]
        return None
    return None


def setTemp(thisId: int, newTemp: list):
    if isExistID(thisId):
        thisData[thisId]["temp"] = newTemp.copy()
        saveData()


def setTempInd(thisId: int, ind: int, data):
    if isExistID(thisId):
        newTemp = getTemp(thisId)
        rem = ind - len(newTemp) + 1
        for i in range(rem):
            newTemp.append("?")
        newTemp[ind] = data
        setTemp(thisId, newTemp)
        saveData()


def getStateKey(thisId: int):
    if isExistID(thisId):
        return thisData[thisId]["stateKey"]
    return 0


def setStateKey(thisId: int, newKey: str):
    if isExistID(thisId):
        thisData[thisId]["stateKey"] = newKey
        saveData()


def makeNewKey(thisId: int) -> str:
    newPKey = cmdUtil.genRandomKey()
    setStateKey(thisId, newPKey)
    return newPKey


def createNewID(thisId: int, messId: int):
    if not isExistID(thisId):
        thisData[thisId] = DEFAULT_DATA.copy()
        thisData[thisId]["CMDmessID"] = messId
        saveData()


def removeID(thisId: int):
    if isExistID(thisId):
        thisData.pop(thisId)
        saveData()


def addMessageId(thisId: int, mesId: int):
    if isExistID(thisId):
        thisData[thisId]["prevMessage"].append(mesId)
        saveData()


def getPrevMess(thisId: int) -> list:
    if isExistID(thisId):
        return thisData[thisId]["prevMessage"].copy()
    return []


def clearPrevMess(thisId: int):
    if isExistID(thisId):
        thisData[thisId]["prevMessage"].clear()
        saveData()


def setVacation(thisId: int, days: int):
    if isExistID(thisId):
        thisData[thisId]["vacationDays"] = days
        saveData()


def getVacation(thisId: int):
    if isExistID(thisId):
        return thisData[thisId]["vacationDays"]
    return 0


def getNotiMode(thisId: int):
    if isExistID(thisId):
        return thisData[thisId]["modeNofi"]
    return "Subject"


def toggleNotiMode(thisId: int):
    if isExistID(thisId):
        if getNotiMode(thisId) == "Subject":
            newOne = "Day"
        else:
            newOne = "Subject"

        thisData[thisId]["modeNofi"] = newOne
        saveData()
        return newOne
    return "Subject"


def getDayOfWeek():
    return serverData["dayOfWeek"]


def setDayOfWeek(day: int):
    serverData["dayOfWeek"] = day
    saveServerData()


def getTimeOfWeek():
    return serverData["timeOfWeek"]


def setTimeOfWeek(timeHashed: int):
    serverData["timeOfWeek"] = timeHashed
    saveServerData()


def addAllServerCReload():
    for s in thisData:
        serverData["chanReload"].append(s)
    saveServerData()


def isCReloadEmpty():
    return len(serverData["chanReload"]) == 0


def popCReload():
    if not isCReloadEmpty():
        x = serverData["chanReload"].pop()
        saveServerData()
        return x


def pushServerSReload(s):
    serverData["timeReload"].append(s)
    saveServerData()


def isSReloadEmpty():
    return len(serverData["timeReload"]) == 0


def popSReload():
    if not isSReloadEmpty():
        x = serverData["timeReload"].pop()
        saveServerData()
        return x


def isNotiDay(thisId: int):
    if isExistID(thisId):
        return thisData[thisId]["modeNofi"] == "Day"
    return False


def setDynaDay(thisId: int, day: int):
    if isExistID(thisId):
        thisData[thisId]["dynamicDay"] = day
        saveData()


def setDynaTime(thisId: int, timu: int):
    if isExistID(thisId):
        thisData[thisId]["dynamicTime"] = timu
        saveData()


def getDyna(thisId: int):
    if isExistID(thisId):
        if isNotiDay(thisId):
            return ("Day", thisData[thisId]["dynamicDay"])
        else:
            return ("Subject", thisData[thisId]["dynamicTime"])
    return -1


def setDMY(day, month, year):
    serverData["dmy"] = [day, month, year]
    saveServerData()


def getDMY():
    return serverData["dmy"].copy()


def reduceVacation(thisId):
    if isExistID(thisId):
        if thisData[thisId]["vacationDays"] > 0:
            thisData[thisId]["vacationDays"] -= 1
            saveData()


def addMissing(thisId):
    if isExistID(thisId):
        thisData[thisId]["missingCrt"] += 1
        saveData()
        return thisData[thisId]["missingCrt"]


def resetMissing(thisId):
    if isExistID(thisId):
        thisData[thisId]["missingCrt"] = 0
        saveData()
