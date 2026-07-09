import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# ======================
# PARAMETRLAR
# ======================
nx, ny = 60, 60
Lx, Ly = 2.0, 2.0
dx = Lx / nx
dy = Ly / ny

nu = 0.1      # viskozlik (mu/rho)
dt = 0.01

# GRID
x = np.linspace(0, Lx, nx)
y = np.linspace(0, Ly, ny)
X, Y = np.meshgrid(x, y)

# boshlang'ich holat (markazda impuls)
u_field = np.zeros((ny, nx))
u_field[ny//2, nx//2] = 5.0

# ======================
# FIGURE
# ======================
fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111, projection='3d')

# ======================
# UPDATE FUNKSIYA
# ======================
def step(u):
    un = u.copy()

    # finite difference
    u[1:-1,1:-1] = (
        un[1:-1,1:-1]
        - dt * un[1:-1,1:-1]*(un[1:-1,1:-1] - un[1:-1,0:-2])/dx
        - dt * un[1:-1,1:-1]*(un[1:-1,1:-1] - un[0:-2,1:-1])/dy
        + nu * dt * (
            (un[1:-1,2:] - 2*un[1:-1,1:-1] + un[1:-1,0:-2]) / dx**2 +
            (un[2:,1:-1] - 2*un[1:-1,1:-1] + un[0:-2,1:-1]) / dy**2
        )
    )

    return u

def update(frame):
    global u_field
    ax.clear()

    u_field = step(u_field)

    surf = ax.plot_surface(X, Y, u_field, cmap='viridis')

    ax.set_title("Navye–Stoks (Dekart, 3D animatsiya)")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Tezlik u(x,y)")

    return surf,

ani = animation.FuncAnimation(fig, update, frames=200, interval=50)

plt.show()