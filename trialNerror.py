from msvcrt import getwch
import random as rng

# for i in range(10):
#     print(rng.randint(1, 4))

# variable = getwch()
# print(variable)

# buttonPos = (
#         [(100 + 100 * i, 100)for i in range(3)],
#         [(300 + 100 * i, 100)for i in range(3)],
#         [(500 + 100 * i, 100)for i in range(3)],
#     )

# print(buttonPos)

# for i in range(9):
#     print((i//3)%3, i%3)

# n = 10
# for lvl in range(100):
#     print(lvl, n)
#     if lvl < 10:
#         n += lvl
#     elif lvl < 20:
#         n += lvl * 2
#     elif lvl < 30:
#         n += lvl * 2
#     else:
#         n += lvl * 10

# Source - https://stackoverflow.com/a/52246129
# Posted by Juan Marín
# Retrieved 2026-02-17, License - CC BY-SA 4.0

# import msvcrt
# import time

# # time.sleep(4)
# while True:
#     while msvcrt.kbhit():
#         flush = input()
#     entry = input("Press enter!")
#     print(entry)

# print(0 % 5)

# DEF = 12
# while DEF:
#     print(DEF)
#     DEF -= DEF // 2 + 1

# ====================================================================

# list = [100 for _ in range(11)]

# aoe = 5
# str = 100

# toAttack = int(input("to attack: "))

# listToAttack = [[toAttack, 1]]
# for i in range(aoe):
#     i += 1
#     listToAttack.append([toAttack + i, (i + 1) / 1.5])
#     listToAttack.append([toAttack - i, (i + 1) / 1.5])
# for attack in listToAttack:
#     if attack[0] >= 0:
#         if attack[0] <= len(list):
#             try:
#                 list[attack[0]] -= int(str / attack[1])
#             except:
#                 print(f"couldnt attack idx: {attack[0]}")
#         else:
#             print("failed attack")
#     else:
#         print("failed attack")

# print(f"attacks: {listToAttack}")
# print(f"enemies: {list}")

# ====================================================================

# temp = 10

# print(eval("temp * 2"))

# list = []

# if list:
#     print("yes")
# else:
#     print("no")

# exp = 5
# totExp = 5

# for lvl in range(1, 50):
#     exp += lvl
#     totExp += exp
#     print(totExp, exp)

# list = [100 for _ in range(11)]

# str = 25
# multi = 5

# toAttack = int(input("to attack: "))

# for attack in range(multi):
#     list[toAttack] -= str // 2 * (attack + 2)
#     print(list[toAttack], str // 2 * (attack + 2))

# print(list)

# import time

# start = time.time()

# time.sleep(10)

# print(time.time() - start)

# runTime = 11111111111
# min = 0
# hours = 0
# days = 0
# while runTime >= 60:
#     runTime -= 60
#     min += 1
#     while min >= 60:
#         min -= 60
#         hours += 1
#         while hours >= 24:
#             hours -= 24
#             days += 1

# if days:
#     print(f"days: {days}, {hours:02d}:{min:02d}:{runTime:02d}")
# elif hours:
#     print(f"{hours:02d}:{min:02d}:{runTime:02d}")
# elif min:
#     print(f"{min:02d}:{runTime:02d}")
# else:
#     print(f"{runTime:02d}")