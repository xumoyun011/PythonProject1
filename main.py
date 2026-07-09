import math

# Parametrlar
a = 1
s = 1.0
t1 = 0.5
h = 0.05
l = 0.05

c = 1 / (h * h)

n = 5
m = 5

# Massivlar
x = [0.0] * 61
t = [0.0] * 61
u = [[0.0 for _ in range(61)] for _ in range(61)]

# Funksiyalar
def fnf(x):
    return 0.2 * x * (1 - x) * math.sin(math.pi * x)

def fnt(x):
    return 0.0

def fnt2(x):
    return 0.0

def fnf1(t):
    return 0.0

def fnf2(t):
    return 0.0

# x qiymatlar
print("   t/x  ", end="")
for i in range(2 * n + 1):
    x[i] = i * h
    print(f"{x[i]:6.3f}", end=" ")
print()

# Chegaraviy shartlar
for j in range(2 * m + 1):
    t[j] = j * l
    u[0][j] = fnf1(t[j])
    u[n][j] = fnf2(t[j])

# Boshlang‘ich shartlar
for i in range(1, 2 * n):
    x[i] = i * h
    u[i][0] = fnf(x[i])

    # 2-usul (siz ishlatgan)
    u[i][1] = (fnf(h * (i + 1)) + fnf(h * (i - 1))) / 2 + l * fnt(h * i)

# Asosiy hisoblash (ayirmali sxema)
for j in range(1, 2 * m):
    for i in range(1, 2 * n):
        u[i][j + 1] = (
            2 * u[i][j]
            - u[i][j - 1]
            + c * (u[i + 1][j] - 2 * u[i][j] + u[i - 1][j])
        )

# Natijani chiqarish
for j in range(2 * m + 1):
    print(f"{t[j]:6.3f} |", end=" ")
    for i in range(2 * n + 1):
        print(f"{u[i][j]:6.3f}", end=" ")
    print()