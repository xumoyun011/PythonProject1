import numpy as np
import matplotlib.pyplot as plt

# Parametrlar
L = 1.0
h = 0.1
eta = 0.001
k = 0.01
z = 1.0
p0_0 = 100.0
p0_L = 20.0

# Grid
x = np.linspace(0, L, 100)
y = np.linspace(-h, h, 100)
X, Y = np.meshgrid(x, y)

# Ko‘makchi ifodalar
sqrt_k = np.sqrt(k)

A = (p0_0*np.exp(-sqrt_k*L) - p0_L) / (np.exp(sqrt_k*L) - np.exp(-sqrt_k*L))
B = (p0_0*np.exp(sqrt_k*L) - p0_L) / (np.exp(sqrt_k*L) - np.exp(-sqrt_k*L))

exp_term1 = np.exp(sqrt_k * X)
exp_term2 = np.exp(-sqrt_k * X)

# u0(x,y)
u0 = (k / (2 * eta)) * (A * exp_term1 + B * exp_term2) * (h**2 - Y**2)

# v0(x,y)
v0 = -(k * z / (2 * eta)) * (A * exp_term1 - B * exp_term2) * (h**2 * Y - Y**3 / 3)

# ====== Grafiklar ======

# 3D grafik (u0)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, u0)
ax.set_title("u0(x,y) tezlik maydoni")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("u0")

plt.show()

# 3D grafik (v0)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, v0)
ax.set_title("v0(x,y) tezlik maydoni")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("v0")

plt.show()

# Kesim (y=0 da)
y0_index = np.argmin(np.abs(y - 0))

plt.figure()
plt.plot(x, u0[y0_index, :])
plt.title("u0(x, 0) kesim")
plt.xlabel("x")
plt.ylabel("u0")
plt.show()

plt.figure()
plt.plot(x, v0[y0_index, :])
plt.title("v0(x, 0) kesim")
plt.xlabel("x")
plt.ylabel("v0")
plt.show()