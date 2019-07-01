import numpy as np
import matplotlib.pyplot as plt

hist = [0]
t = [0]
speed = -400
Kp = 0.1


vitesse = 0
for i in range(50):
    er = speed - vitesse
    vitesse = vitesse + er*Kp
    hist.append(vitesse)
    t.append(i)

plt.plot(t,hist)
plt.show()
