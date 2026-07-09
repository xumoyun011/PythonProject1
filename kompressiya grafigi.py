import matplotlib.pyplot as plt
import numpy as np

# Misol ma'lumotlar
# Bosimlar σ (kPa)
sigma = np.array([50, 100, 200, 400, 800])

# Bo'shliqlik koeffitsiyenti e
e = np.array([0.95, 0.85, 0.75, 0.65, 0.55])

# log(σ) hisoblash
log_sigma = np.log10(sigma)

# Grafik chizish
plt.figure(figsize=(8,6))
plt.plot(log_sigma, e, marker='o', linestyle='-', color='blue', label="Kompressiya egri chizig‘i")
plt.xlabel("log(σ), kPa")
plt.ylabel("e (bo'shliqlik koeffitsiyenti)")
plt.title("Gruntning kompressiya egri chizig‘i")
plt.grid(True)
plt.legend()
plt.show()