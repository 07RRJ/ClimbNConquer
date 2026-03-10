import sys, os

def GetGameFolder():
    return getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))

def ResourcePath(relative_path, path = False):
    if not path:
        return os.path.join(GetGameFolder(), relative_path)
    else:
        return os.path.join(path, relative_path)

def Attack(STR, enemy):
    if STR:
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