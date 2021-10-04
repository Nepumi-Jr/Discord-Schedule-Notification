import datetime
import time


def hash(epochTime: int) -> int:
    # ? 864 is 0
    res = epochTime % (60*60*24*7) // (5 * 60)
    # *                    ^ จำนวนวินาทีในหนึ่งสัปดาห์
    res = (res-864+2016) % 2016
    return res


def hashBack(timeHased: int) -> tuple:
    thaiDay=["วันอาทิตย์","วันจันทร์","วันอังคาร","วันพุธ","วันพฤหัสบดี","วันศุกร์","วันเสาร์",]
    hour = int((timeHased * 5) / 60)
    day = int(hour / 24)
    hour = hour - (day*24)
    if day >= 7:
        day = day % 7
    minute = (timeHased * 5) % 60
    day = thaiDay[day]

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

def main():
    for i in range(2016):
        print(i,end=" ")
        print(hashBack(i))
  

if __name__ == "__main__":
    main()
