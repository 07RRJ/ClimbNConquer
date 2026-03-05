from msvcrt import getwch

# variable = getwch()
# print(variable)

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

list = [5]

aoe = 1
str = 1

toAttack = int(input("to attack: "))

listToAttack = [[toAttack, 1]]
for i in range(aoe):
    i += 1
    listToAttack.append([toAttack + i, i + 1])
    listToAttack.append([toAttack - i, i + 1])
for attack in listToAttack:
    if attack[0] >= 0:
        if attack[0] <= len(list):
            try:
                list[attack[0]] -= str // attack[1]
            except:
                print(f"couldnt attack idx: {attack[0]}")

print(listToAttack)
print(list)