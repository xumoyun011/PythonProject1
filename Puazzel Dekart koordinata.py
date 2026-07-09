import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

# ---------- FUNCTION ----------
def solve_and_plot():
    try:
        mu = float(entry_mu.get())
        h = float(entry_h.get())
        dPdx = float(entry_dpdx.get())
        N = int(entry_N.get())
    except:
        print("Invalid input")
        return

    dy = h / (N - 1)
    y = np.linspace(0, h, N)

    # Numerical solution
    A = np.zeros((N, N))
    b = np.zeros(N)

    A[0, 0] = 1
    A[-1, -1] = 1

    for i in range(1, N-1):
        A[i, i-1] = 1
        A[i, i] = -2
        A[i, i+1] = 1
        b[i] = (dPdx / mu) * dy**2

    v_num = np.linalg.solve(A, b)

    # Analytical solution
    v_ana = (1/(2*mu))*dPdx*(y**2 - h*y)

    # Error
    error = np.abs(v_num - v_ana)
    min_index = np.argmin(error)

    print("\n=== Comparison ===")
    for i in range(N):
        print(f"y={y[i]:.3f}  num={v_num[i]:.5f}  ana={v_ana[i]:.5f}  err={error[i]:.2e}")

    print("Best match at y =", y[min_index])

    # Plot
    plt.figure()
    plt.plot(v_ana, y, label='Analytical')
    plt.plot(v_num, y, 'o--', label='Numerical')
    plt.scatter(v_num[min_index], y[min_index], s=100)
    plt.title('Poiseuille Flow Comparison')
    plt.xlabel('Velocity')
    plt.ylabel('y')
    plt.legend()
    plt.grid()
    plt.show()

# ---------- GUI ----------
root = tk.Tk()
root.title("Poiseuille Solver")

frame = ttk.Frame(root, padding=10)
frame.grid()

# Inputs
ttk.Label(frame, text="mu").grid(column=0, row=0)
entry_mu = ttk.Entry(frame)
entry_mu.insert(0, "1.0")
entry_mu.grid(column=1, row=0)

ttk.Label(frame, text="h").grid(column=0, row=1)
entry_h = ttk.Entry(frame)
entry_h.insert(0, "1.0")
entry_h.grid(column=1, row=1)

ttk.Label(frame, text="dP/dx").grid(column=0, row=2)
entry_dpdx = ttk.Entry(frame)
entry_dpdx.insert(0, "-1.0")
entry_dpdx.grid(column=1, row=2)

ttk.Label(frame, text="N (grid)").grid(column=0, row=3)
entry_N = ttk.Entry(frame)
entry_N.insert(0, "20")
entry_N.grid(column=1, row=3)

# Button
btn = ttk.Button(frame, text="Hisoblash", command=solve_and_plot)
btn.grid(column=0, row=4, columnspan=2, pady=10)

root.mainloop()