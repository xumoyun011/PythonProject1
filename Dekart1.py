import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ---------------- PARAMETERS ----------------
mu = 1.0
h = 1.0
dPdx = -1.0
Ny = 30
Nt = 80

dy = h / (Ny - 1)
dt = 0.002

y = np.linspace(0, h, Ny)
t = np.linspace(0, Nt * dt, Nt)

# ---------------- INITIAL ----------------
v = np.zeros(Ny)
V_time = []

# ---------------- STEP-BY-STEP SOLUTION ----------------
for step in range(Nt):
    v_new = v.copy()

    for i in range(1, Ny - 1):
        # diffusion term (Dekart)
        d2v = (v[i + 1] - 2 * v[i] + v[i - 1]) / dy ** 2

        # update
        v_new[i] = v[i] + dt * (mu * d2v - dPdx)

    # boundary conditions
    v_new[0] = 0
    v_new[-1] = 0

    v = v_new.copy()
    V_time.append(v.copy())

    # ----------- STEP VISUALIZATION -----------
    if step % 10 == 0:
        plt.figure()
        plt.plot(v, y)
        plt.title(f"Step {step}")
        plt.xlabel("Velocity")
        plt.ylabel("y")
        plt.grid()
        plt.show()

# Convert to array
V_time = np.array(V_time)

# ---------------- 3D VISUALIZATION ----------------
T, Y = np.meshgrid(t, y)
V_plot = V_time.T

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(T, Y, V_plot, cmap='plasma')

# Color scale
fig.colorbar(surf, ax=ax, shrink=0.6, aspect=10, label='Velocity')

# Labels
ax.set_xlabel('Time (t)')
ax.set_ylabel('y (channel height)')
ax.set_zlabel('Velocity v')
ax.set_title('3D Unsteady Poiseuille Flow (Cartesian, Step-by-Step)')

plt.show()