import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline

h = 200 # horisontal avstand mellom yfast
xfast = np.asarray([0,h,2*h,3*h,4*h,5*h,6*h,7*h])
yfast = np.asarray([0.291, 0.248, 0.179, 0.135, 0.12, 0.126, 0.089, 0.016])
xfast = xfast/1000

# scipy.interpolate-funksjonen CubicSpline:
cs = CubicSpline(xfast, yfast, bc_type='natural')
xmin = 0.000
xmax = 1.401
dx = 0.001
x = np.arange(xmin, xmax, dx)
Nx = len(x)
y = cs(x)
dy = cs(x,1)
d2y = cs(x,2)


# Krumningsradius, obviosly
krumningsRadius = []
for i in range(0, len(d2y)):
    krum_rad = ((d2y[i]) / (1+(dy[i])**2)**(1.5))
    krumningsRadius.append(krum_rad)

# Plot
baneform = plt.figure('f/n',figsize=(12,6))
plt.plot(x,krumningsRadius,xfast,yfast," ")
plt.title('f/n')
plt.xlabel('x(m)',fontsize=12)  
plt.ylabel('|f/n|',fontsize=12)
plt.ylim(-1.7, 1.2)
plt.grid()
plt.show()
