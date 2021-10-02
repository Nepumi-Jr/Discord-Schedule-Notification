import datetime
import time


def hash(epochTime: int) -> int:
    # Zeller’s Rule
    # f=k + [(13 * m-1)/5] + d + [d / 4] +[c / 4]-(2 * c)
    # where
    # k is  the day of the month.
    # m is the month number.
    # d is the last two digits of the year.
    # c is the first two digits of the year.
    a = str(datetime.datetime.utcfromtimestamp(
        epochTime).replace(tzinfo=datetime.timezone.utc))
    date = a.split()  # split string with " "
    time = date[1]  # get time
    date = date[0]  # get date
    date = date.split("-")  # split date 22/04/2002 to '22','04','2002'

    # Zeller's rule variable
    k = int(date[2])
    m = int(date[1])
    m = m + 10
    if m > 12:
        m = m % 12
    d = int(date[0][2:])
    c = int(date[0][0:2])

    # convert hour to minute
    GMT = 7
    time = time[0:8]
    hour = int(time[0:2]) + GMT
    if hour > 24:
        hour = hour % 24
        k = k + 1
    minute = int(time[3:5])

    # Find a day in week
    f = k + int((13*m-1)/5) + d + int(d / 4) + int(c / 4) - int(2 * c)
    day = (f % 7)

    # Sum of minute
    completelyMinute = minute + (hour * 60) + (day * 24 * 60)

    # any number in every 5 minute in epoch time
    result = int(completelyMinute / 5)

    return result % 2016


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
    # print(hash(1632026672))
    for i in range(2016):
        print(i, hashBack(i))


if __name__ == "__main__":
    main()
