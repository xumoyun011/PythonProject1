import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

# =========================
# PARAMETRLAR
# =========================
R0 = 1.0
L0 = 5.0
mu0 = 1.0
dP0 = 10.0

# =========================
# ANALITIK YECHIM
# =========================
def velocity_profile(r, R, mu, dP, L):
    return (dP / (4 * mu * L)) * (R**2 - r**2)

# =========================
# SONLI YECHIM (Finite Difference)
# =========================
def numerical_solution(R, mu, dP, L, N=100):
    dr = R / N
    r = np.linspace(0, R, N)

    A = np.zeros((N, N))
    b = np.ones(N) * (-dP / (mu * L))

    for i in range(1, N-1):
        A[i, i-1] = 1
        A[i, i] = -2
        A[i, i+1] = 1

    # boundary conditions
    A[0,0] = 1      # center symmetry
    A[-1,-1] = 1    # wall v=0
    b[0] = 0
    b[-1] = 0

    v = np.linalg.solve(A, b) * dr**2
    return r, v

# =========================
# GRID
# =========================
theta = np.linspace(0, 2*np.pi, 60)
r = np.linspace(0, R0, 60)
theta, r = np.meshgrid(theta, r)

def compute_surface(R, mu, dP, L):
    X = r * np.cos(theta)
    Y = r * np.sin(theta)
    V = velocity_profile(r, R, mu, dP, L)
    return X, Y, V

# =========================
# FIGURE
# =========================
fig = plt.figure(figsize=(14, 8))
ax = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122)

plt.subplots_adjust(bottom=0.25)

# initial plot
X, Y, V = compute_surface(R0, mu0, dP0, L0)
surf = ax.plot_surface(X, Y, V, cmap='viridis')

# analytical vs numerical
r_num, v_num = numerical_solution(R0, mu0, dP0, L0)
v_anal = velocity_profile(r_num, R0, mu0, dP0, L0)

line1, = ax2.plot(r_num, v_anal, label="Analitik")
line2, = ax2.plot(r_num, v_num, '--', label="Sonli")

ax2.legend()
ax2.set_title("Analitik vs Sonli yechim")

# =========================
# SLIDERLAR
# =========================
axcolor = 'lightgoldenrodyellow'

ax_R = plt.axes([0.2, 0.15, 0.6, 0.03], facecolor=axcolor)
ax_mu = plt.axes([0.2, 0.10, 0.6, 0.03], facecolor=axcolor)
ax_dP = plt.axes([0.2, 0.05, 0.6, 0.03], facecolor=axcolor)

sR = Slider(ax_R, 'R', 0.5, 2.0, valinit=R0)
sMu = Slider(ax_mu, 'mu', 0.1, 5.0, valinit=mu0)
sDP = Slider(ax_dP, 'dP', 1.0, 20.0, valinit=dP0)

# =========================
# UPDATE FUNKSIYA
# =========================
def update(val):
    ax.clear()
    ax2.clear()

    R = sR.val
    mu = sMu.val
    dP = sDP.val

    X, Y, V = compute_surface(R, mu, dP, L0)
    ax.plot_surface(X, Y, V, cmap='viridis')

    r_num, v_num = numerical_solution(R, mu, dP, L0)
    v_anal = velocity_profile(r_num, R, mu, dP, L0)

    ax2.plot(r_num, v_anal, label="Analitik")
    ax2.plot(r_num, v_num, '--', label="Sonli")

    ax2.legend()
    ax.set_title("3D oqim")
    ax2.set_title("Taqqoslash")

    fig.canvas.draw_idle()

sR.on_changed(update)
sMu.on_changed(update)
sDP.on_changed(update)

# =========================
# ANIMATSIYA
# =========================
def animate(i):
    ax.clear()
    R = R0
    mu = mu0
    dP = dP0 + 5*np.sin(i/10)

    X, Y, V = compute_surface(R, mu, dP, L0)
    ax.plot_surface(X, Y, V, cmap='plasma') 
    ax.set_title("Animatsiya (bosim o'zgaradi)")

ani = animation.FuncAnimation(fig, animate, frames=100, interval=100)

plt.show()