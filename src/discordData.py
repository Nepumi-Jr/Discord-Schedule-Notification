import yaml
from src import cmdUtil

thisData = dict()
DEFAULT_DATA = {
    "modeNofi": "Subject",
    "CMDmessID": 69
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


def changeMessID(thisId: int, messId: int):
    if isExistID(thisId):
        thisData[thisId]["CMDmessID"] = messId
        saveData()


def getMessID(thisId: int):
    if isExistID(thisId):
        return thisData[thisId]["CMDmessID"]
    return 0


def createNewID(thisId: int, messId: int):
    if not isExistID(thisId):
        thisData[thisId] = DEFAULT_DATA.copy()
        thisData[thisId]["CMDmessID"] = messId
        saveData()


def removeID(thisId: int):
    if isExistID(thisId):
        thisData.pop(thisId)
        saveData()
