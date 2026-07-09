import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# ======================
# PARAMETRLAR
# ======================
nx, ny = 50, 50
Lx, Ly = 2.0, 2.0
dx = Lx/(nx-1)
dy = Ly/(ny-1)

rho = 1.0
nu = 0.1
dt = 0.01

# GRID
x = np.linspace(0, Lx, nx)
y = np.linspace(0, Ly, ny)
X, Y = np.meshgrid(x, y)

# boshlang‘ich maydonlar
u_field = np.zeros((ny, nx))
v_field = np.zeros((ny, nx))
p = np.zeros((ny, nx))

# boshlang‘ich impuls
u_field[ny//2, nx//2] = 2.0

# ======================
# BOSIM POISSON
# ======================
def pressure_poisson(p, dx, dy, b):
    pn = p.copy()
    for _ in range(30):
        p[1:-1,1:-1] = (
            (pn[1:-1,2:] + pn[1:-1,0:-2])*dy**2 +
            (pn[2:,1:-1] + pn[0:-2,1:-1])*dx**2
        ) / (2*(dx**2 + dy**2)) - \
        dx**2 * dy**2 / (2*(dx**2 + dy**2)) * b[1:-1,1:-1]

        # boundary
        p[:,-1] = p[:,-2]
        p[:,0] = p[:,1]
        p[0,:] = p[1,:]
        p[-1,:] = 0
        pn = p.copy()
    return p

# ======================
# STEP
# ======================
def step(u, v, p):
    un = u.copy()
    vn = v.copy()

    b = np.zeros_like(p)

    b[1:-1,1:-1] = (
        rho*(1/dt*((un[1:-1,2:]-un[1:-1,0:-2])/(2*dx) +
                   (vn[2:,1:-1]-vn[0:-2,1:-1])/(2*dy))
        - ((un[1:-1,2:]-un[1:-1,0:-2])/(2*dx))**2
        - 2*((un[2:,1:-1]-un[0:-2,1:-1])/(2*dy) *
             (vn[1:-1,2:]-vn[1:-1,0:-2])/(2*dx))
        - ((vn[2:,1:-1]-vn[0:-2,1:-1])/(2*dy))**2)
    )

    p = pressure_poisson(p, dx, dy, b)

    u[1:-1,1:-1] = (
        un[1:-1,1:-1]
        - un[1:-1,1:-1]*dt/dx*(un[1:-1,1:-1]-un[1:-1,0:-2])
        - vn[1:-1,1:-1]*dt/dy*(un[1:-1,1:-1]-un[0:-2,1:-1])
        - dt/(rho*2*dx)*(p[1:-1,2:]-p[1:-1,0:-2])
        + nu*(dt/dx**2*(un[1:-1,2:]-2*un[1:-1,1:-1]+un[1:-1,0:-2]) +
              dt/dy**2*(un[2:,1:-1]-2*un[1:-1,1:-1]+un[0:-2,1:-1]))
    )

    v[1:-1,1:-1] = (
        vn[1:-1,1:-1]
        - un[1:-1,1:-1]*dt/dx*(vn[1:-1,1:-1]-vn[1:-1,0:-2])
        - vn[1:-1,1:-1]*dt/dy*(vn[1:-1,1:-1]-vn[0:-2,1:-1])
        - dt/(rho*2*dy)*(p[2:,1:-1]-p[0:-2,1:-1])
        + nu*(dt/dx**2*(vn[1:-1,2:]-2*vn[1:-1,1:-1]+vn[1:-1,0:-2]) +
              dt/dy**2*(vn[2:,1:-1]-2*vn[1:-1,1:-1]+vn[0:-2,1:-1]))
    )

    # boundary
    u[0,:]=0; u[-1,:]=0; u[:,0]=0; u[:,-1]=0
    v[0,:]=0; v[-1,:]=0; v[:,0]=0; v[:,-1]=0

    return u, v, p

# ======================
# FIGURE
# ======================
fig = plt.figure(figsize=(12,6))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122, projection='3d')

def update(frame):
    global u_field, v_field, p
    ax1.clear()
    ax2.clear()

    u_field, v_field, p = step(u_field, v_field, p)

    speed = np.sqrt(u_field**2 + v_field**2)

    # 🔹 quiver
    ax1.quiver(X, Y, u_field, v_field)
    ax1.set_title("Vektor maydon (u,v)")
    ax1.set_xlabel("X"); ax1.set_ylabel("Y")

    # 🔹 3D surface
    surf = ax2.plot_surface(X, Y, speed, cmap='viridis')
    ax2.set_title("Tezlik moduli |v|")
    ax2.set_xlabel("X"); ax2.set_ylabel("Y")
    ax2.set_zlabel("|v|")

    return surf,

ani = animation.FuncAnimation(fig, update, frames=150, interval=50)

plt.show()