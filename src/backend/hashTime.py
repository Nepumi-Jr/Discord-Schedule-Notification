import datetime
import time


def hash(epochTime: int) -> int:
    # ? 864 is 0
    res = epochTime % (60*60*24*7) // (5 * 60)
    # *                    ^ จำนวนวินาทีในหนึ่งสัปดาห์
    res = (res-864+2016) % 2016
    return res


def hashBack(timeHased: int) -> tuple:
    # TODO : เหมือน Hash แต่รับข้อมูลเป็นเวลาที่ถูก hash
    # TODO : ให้ส่งค่าออกมาเป็น string ภาษาไทยที่สวยงาม

    # ! skrrt
    hour = int((timeHased * 5) / 60)
    day = 0
    if hour >= 24:
        day = hour % 23
        hour = hour - (day*24)
    if day >= 7:
        day = day % 7
    minute = (timeHased * 5) % 60
    day = thaiDay(day)

    # make turn int to time format
    if hour < 10:
        hour = "0" + str(hour)
    else:
        hour = str(hour)
    if minute < 10:
        minute = "0" + str(minute)
    else:
        minute = str(minute)
    time = hour + ":" + minute + " น."
    return (day, time)


def thaiDay(numOfDay: int) -> str:
    if numOfDay == 0:
        return "วันอาทิตย์"
    elif numOfDay == 1:
        return "วันจันทร์"
    elif numOfDay == 2:
        return "วันอังคาร"
    elif numOfDay == 3:
        return "วันพุธ"
    elif numOfDay == 4:
        return "วันพฤหัสบดี"
    elif numOfDay == 5:
        return "วันศุกร์"
    elif numOfDay == 6:
        return "วันวันเสาร์"


def main():
    print(hash(1633325510 + 60*60*7))
    # for i in range(2016):
    #     print(i, hashBack(i))


if __name__ == "__main__":
    main()
