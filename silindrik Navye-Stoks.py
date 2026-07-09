import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# ======================
# PARAMETRLAR
# ======================
nr, nth = 50, 80
r_min, r_max = 0.3, 1.0

dr = (r_max - r_min)/(nr-1)
dth = 2*np.pi/(nth-1)

rho = 1.0
nu = 0.05
dt = 0.001
nt = 300

r = np.linspace(r_min, r_max, nr)
th = np.linspace(0, 2*np.pi, nth)

R, TH = np.meshgrid(r, th)

# Maydonlar
ur  = np.zeros((nth, nr))
uth = np.zeros((nth, nr))
p   = np.zeros((nth, nr))

# kichik boshlang‘ich perturbatsiya (tezroq "uyg‘onishi" uchun)
uth += 0.05*np.sin(TH)

# ======================
# YORDAMCHI FUNKSIYALAR
# ======================
def laplacian(f):
    """Silindrik Laplasian (soddalashtirilgan, markazdan qochilgan)."""
    L = np.zeros_like(f)
    for i in range(1, nth-1):
        for j in range(1, nr-1):
            rj = r[j]
            L[i,j] = (
                (f[i,j+1] - 2*f[i,j] + f[i,j-1]) / dr**2 +
                (1/rj) * (f[i,j+1] - f[i,j-1]) / (2*dr) +
                (f[i+1,j] - 2*f[i,j] + f[i-1,j]) / (rj**2 * dth**2)
            )
    return L

def divergence(ur, uth):
    """∇·u silindrikda."""
    div = np.zeros_like(ur)
    for i in range(1, nth-1):
        for j in range(1, nr-1):
            rj = r[j]
            div[i,j] = (
                (1/rj) * ( (r[j+1]*ur[i,j+1] - r[j-1]*ur[i,j-1]) / (2*dr) ) +
                (uth[i+1,j] - uth[i-1,j]) / (2*rj*dth)
            )
    return div

def pressure_poisson(p, rhs, iters=60):
    """∇²p = rhs ni Gauss–Seidel bilan yechish."""
    for _ in range(iters):
        pn = p.copy()
        for i in range(1, nth-1):
            for j in range(1, nr-1):
                rj = r[j]
                p[i,j] = (
                    (pn[i,j+1] + pn[i,j-1]) / dr**2 +
                    (pn[i+1,j] + pn[i-1,j]) / (rj**2 * dth**2) -
                    rhs[i,j]
                ) / (2/dr**2 + 2/(rj**2 * dth**2))

        # Chegaralar
        p[:, 0]  = p[:, 1]     # inner Neumann
        p[:, -1] = 0.0         # outer Dirichlet (gauge)
        p[0, :]  = p[-2, :]    # periodic θ
        p[-1, :] = p[1,  :]    # periodic θ
    return p

# ======================
# ANIMATSIYA
# ======================
fig, ax = plt.subplots(figsize=(6,6))

def animate(n):
    global ur, uth, p

    ur_old  = ur.copy()
    uth_old = uth.copy()

    # 1) Oraliq tezlik (bosimsiz)
    for i in range(1, nth-1):
        for j in range(1, nr-1):
            rj = r[j]

            # konveksiya (upwind emas, markaziy — soddalashtirilgan)
            adv_ur = (
                ur_old[i,j] * (ur_old[i,j] - ur_old[i,j-1]) / dr +
                uth_old[i,j] * (ur_old[i,j] - ur_old[i-1,j]) / (rj*dth)
            )
            adv_uth = (
                ur_old[i,j] * (uth_old[i,j] - uth_old[i,j-1]) / dr +
                uth_old[i,j] * (uth_old[i,j] - uth_old[i-1,j]) / (rj*dth)
            )

            # geometrik hadlar
            geo_ur  = -(uth_old[i,j]**2) / rj
            geo_uth =  (ur_old[i,j]*uth_old[i,j]) / rj

            # diffuziya
            diff_ur  = nu * laplacian(ur_old)[i,j]
            diff_uth = nu * laplacian(uth_old)[i,j]

            ur[i,j]  = ur_old[i,j]  + dt * ( -adv_ur  + geo_ur  + diff_ur )
            uth[i,j] = uth_old[i,j] + dt * ( -adv_uth - geo_uth + diff_uth )

    # 2) Chegaraviy shartlar (no-slip)
    uth[:, -1] = 2.0   # tashqi devor aylansin
    ur[:,  -1] = 0.0

    uth[:,  0] = 0.0   # ichki devor
    ur[:,   0] = 0.0

    # θ-periodik
    ur[0,:]  = ur[-2,:]
    ur[-1,:] = ur[1,:]
    uth[0,:] = uth[-2,:]
    uth[-1,:]= uth[1,:]

    # 3) Divergensiya va bosim
    div = divergence(ur, uth)
    rhs = (rho/dt) * div
    p = pressure_poisson(p, rhs, iters=60)

    # 4) Tuzatish (bosim gradienti bilan)
    for i in range(1, nth-1):
        for j in range(1, nr-1):
            rj = r[j]
            dp_dr   = (p[i,j+1] - p[i,j-1]) / (2*dr)
            dp_dth  = (p[i+1,j] - p[i-1,j]) / (2*dth)

            ur[i,j]  -= (dt/rho) * dp_dr
            uth[i,j] -= (dt/rho) * (1/rj) * dp_dth

    # Chegaralarni yana tiklash
    uth[:, -1] = 2.0; ur[:, -1] = 0.0
    uth[:,  0] = 0.0; ur[:,  0] = 0.0
    ur[0,:]  = ur[-2,:]; ur[-1,:]  = ur[1,:]
    uth[0,:] = uth[-2,:]; uth[-1,:]= uth[1,:]

    # Vizualizatsiya (kartesiyanga o‘tkazib)
    X = R*np.cos(TH)
    Y = R*np.sin(TH)

    U = ur*np.cos(TH) - uth*np.sin(TH)
    V = ur*np.sin(TH) + uth*np.cos(TH)

    speed = np.sqrt(U**2 + V**2)

    ax.clear()
    ax.contourf(X, Y, speed, levels=30)
    ax.quiver(X[::3,::3], Y[::3,::3], U[::3,::3], V[::3,::3])
    ax.set_aspect('equal')
    ax.set_title(f"Step {n}")

anim = animation.FuncAnimation(fig, animate, frames=nt, interval=30)
plt.show()