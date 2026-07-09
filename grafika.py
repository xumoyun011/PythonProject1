import numpy as np
import matplotlib.pyplot as plt

# x qiymatlari
x = np.linspace(0.1, 5, 1000)

# F(x,y)=0 dan y ni ifodalash
y1 = (2*x**2 + 1)/x - 5

# G(x,y)=0 dan y ni ifodalash
y2 = np.sqrt(x + 3*np.log10(x))
y3 = -np.sqrt(x + 3*np.log10(x))

# Grafik
plt.figure(figsize=(8,6))

plt.plot(x, y1, label=r'$F(x,y)=0$')
plt.plot(x, y2, label=r'$G(x,y)=0$')
plt.plot(x, y3)

plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.title('Tenglamalar sistemasining grafigi')

plt.show()