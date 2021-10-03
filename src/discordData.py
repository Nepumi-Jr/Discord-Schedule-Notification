import yaml
from src import cmdUtil

thisData = dict()
DEFAULT_DATA = {
    "modeNofi": "Subject",
    "state": "idle",
    "stateKey": "AAAAA",
    "CMDmessID": 69,
    "temp": [],
    "prevMessage": []
}


def saveData():
    global thisData
    with open("disData.yml", "w") as f:
        yaml.dump(thisData, f)


def validData():
    if not thisData:
        return
    for e in thisData:
        for f in DEFAULT_DATA:
            if f not in thisData[e]:
                thisData[e][f] = DEFAULT_DATA[f]

    saveData()


def loadData():
    global thisData
    cmdUtil.fileExist("disData.yml")
    with open("disData.yml", "r") as f:
        thisData = yaml.load(f, Loader=yaml.FullLoader)

    if thisData == None:
        thisData = dict()

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


def getStateKey(thisId: int) -> str:
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
