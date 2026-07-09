import torch
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

nx, ny = 80, 80
Lx, Ly = 2.0, 2.0
dx = Lx/(nx-1)
dy = Ly/(ny-1)

rho = 1.0
nu = 0.05
dt = 0.01

# grid
x = torch.linspace(0, Lx, nx, device=device)
y = torch.linspace(0, Ly, ny, device=device)
X, Y = torch.meshgrid(x, y, indexing='ij')

# fields
u = torch.zeros((nx, ny), device=device)
v = torch.zeros((nx, ny), device=device)
p = torch.zeros((nx, ny), device=device)

# 🔥 KUCHLI BOSHLANG‘ICH IMPULS
u[nx//2-5:nx//2+5, ny//2-5:ny//2+5] = 5.0

def pressure_poisson(p, b):
    for _ in range(30):
        pn = p.clone()
        p[1:-1,1:-1] = (
            (pn[1:-1,2:] + pn[1:-1,0:-2])*dy**2 +
            (pn[2:,1:-1] + pn[0:-2,1:-1])*dx**2
        ) / (2*(dx**2 + dy**2)) - \
        dx**2 * dy**2 / (2*(dx**2 + dy**2)) * b[1:-1,1:-1]

        p[:, -1] = p[:, -2]
        p[:, 0] = p[:, 1]
        p[0, :] = p[1, :]
        p[-1, :] = 0
    return p

def step(u, v, p):
    un = u.clone()
    vn = v.clone()

    b = torch.zeros_like(p)

    b[1:-1,1:-1] = (
        rho*(1/dt*((un[1:-1,2:]-un[1:-1,0:-2])/(2*dx) +
                   (vn[2:,1:-1]-vn[0:-2,1:-1])/(2*dy)))
    )

    p = pressure_poisson(p, b)

    u[1:-1,1:-1] = (
        un[1:-1,1:-1]
        + nu*(dt/dx**2*(un[1:-1,2:]-2*un[1:-1,1:-1]+un[1:-1,0:-2]) +
              dt/dy**2*(un[2:,1:-1]-2*un[1:-1,1:-1]+un[0:-2,1:-1]))
    )

    v[1:-1,1:-1] = (
        vn[1:-1,1:-1]
        + nu*(dt/dx**2*(vn[1:-1,2:]-2*vn[1:-1,1:-1]+vn[1:-1,0:-2]) +
              dt/dy**2*(vn[2:,1:-1]-2*vn[1:-1,1:-1]+vn[0:-2,1:-1]))
    )

    return u, v, p

fig, ax = plt.subplots(figsize=(6,6))

def update(frame):
    global u, v, p

    for _ in range(5):
        u, v, p = step(u, v, p)

    speed = torch.sqrt(u**2 + v**2).cpu().numpy()

    ax.clear()

    # 🔥 rangli maydon
    im = ax.imshow(speed, origin='lower', cmap='viridis', vmin=0, vmax=5)

    # 🔥 vector field
    skip = 5
    ax.quiver(
        X.cpu().numpy()[::skip,::skip],
        Y.cpu().numpy()[::skip,::skip],
        u.cpu().numpy()[::skip,::skip],
        v.cpu().numpy()[::skip,::skip],
        color='white'
    )

    ax.set_title("GPU Navye–Stoks (real ko‘rinish)")
    return [im]

ani = animation.FuncAnimation(fig, update, frames=200, interval=50)

plt.show()