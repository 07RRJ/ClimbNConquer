from msvcrt import getwch
from os import system

def cls():
    system("cls")

def Attack(STR, enemy):
    if STR:
        print(STR)
        if STR >= enemy.DEF + enemy.HP:
            enemy.DEF = 0
            enemy.HP = 0
        elif enemy.DEF:
            enemy.DEF -= STR
            if enemy.DEF < 0:
                enemy.HP += enemy.DEF
                enemy.DEF = 0
        else:
            enemy.HP -= STR

def Limit(question, Min, Max):
    while True:
        try:
            print(question)
            value = int(getwch())
            if value > Min:
                if value < Max:
                    return value
        except:
            pass

def Comfirm(input):
    if getwch().lower() == input:
        return True

def GetTime(sec, endTime = False):
    if endTime:
        sec = int(endTime - sec)
    min = 0
    hours = 0
    days = 0
    while sec >= 60:
        sec -= 60
        min += 1
        while min >= 60:
            min -= 60
            hours += 1
            while hours >= 24:
                hours -= 24
                days += 1

    if days:
        return f"days: {days}, {hours:02d}:{min:02d}:{sec:02d}"
    elif hours:
        return f"{hours:02d}:{min:02d}:{sec:02d} hours"
    elif min:
        return f"{min:02d}:{sec:02d} minutes"
    else:
        return f"{sec} seconds"