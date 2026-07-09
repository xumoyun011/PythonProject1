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
dt = 0.002
nt = 300

r = np.linspace(r_min, r_max, nr)
th = np.linspace(0, 2*np.pi, nth)

R, TH = np.meshgrid(r, th)

# tezliklar
ur = np.zeros((nth, nr))
uth = np.zeros((nth, nr))

# 🔥 boshlang‘ich perturbatsiya
uth = 0.2*np.sin(TH)

# ======================
# ANIMATSIYA
# ======================
fig, ax = plt.subplots(figsize=(6,6))

def animate(n):
    global ur, uth

    ur_old = ur.copy()
    uth_old = uth.copy()

    for i in range(1, nth-1):
        for j in range(1, nr-1):
            rj = r[j]

            # radial
            ur[i,j] = (
                ur_old[i,j]
                - dt * ur_old[i,j]*(ur_old[i,j]-ur_old[i,j-1])/dr
                - dt * uth_old[i,j]*(ur_old[i,j]-ur_old[i-1,j])/(rj*dth)
                + dt * (uth_old[i,j]**2)/rj
                + nu*dt*(
                    (ur_old[i,j+1]-2*ur_old[i,j]+ur_old[i,j-1])/dr**2 +
                    (ur_old[i+1,j]-2*ur_old[i,j]+ur_old[i-1,j])/(rj**2*dth**2)
                )
            )

            # theta
            uth[i,j] = (
                uth_old[i,j]
                - dt * ur_old[i,j]*(uth_old[i,j]-uth_old[i,j-1])/dr
                - dt * uth_old[i,j]*(uth_old[i,j]-uth_old[i-1,j])/(rj*dth)
                - dt * ur_old[i,j]*uth_old[i,j]/rj
                + nu*dt*(
                    (uth_old[i,j+1]-2*uth_old[i,j]+uth_old[i,j-1])/dr**2 +
                    (uth_old[i+1,j]-2*uth_old[i,j]+uth_old[i-1,j])/(rj**2*dth**2)
                )
            )

    # ======================
    # CHEGARAVIY SHARTLAR
    # ======================
    uth[:,-1] = 2.0   # tashqi devor aylansin
    ur[:,-1] = 0

    uth[:,0] = 0
    ur[:,0] = 0

    # ======================
    # KARTESIYANGA O‘TKAZISH
    # ======================
    X = R*np.cos(TH)
    Y = R*np.sin(TH)

    U = ur*np.cos(TH) - uth*np.sin(TH)
    V = ur*np.sin(TH) + uth*np.cos(TH)

    speed = np.sqrt(U**2 + V**2)

    ax.clear()

    # 🔥 rangli tezlik xaritasi
    ax.contourf(X, Y, speed, levels=30)

    # 🔥 vektorlar (har 3-tadan bittasini chizamiz)
    ax.quiver(X[::3, ::3], Y[::3, ::3],
              U[::3, ::3], V[::3, ::3])

    ax.set_aspect('equal')
    ax.set_title(f"Step {n}")

# ======================
# ISHLATISH
# ======================
anim = animation.FuncAnimation(fig, animate, frames=nt, interval=30)
plt.show()