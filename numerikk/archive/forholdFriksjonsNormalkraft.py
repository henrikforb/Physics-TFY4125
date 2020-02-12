import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline

g = -9.81 # Gravitasjonskonstanten
M = 0.030 # Massen til objektet vi skal bruke i forsøket
c1 = 0.5 # C for den kompakte skiva (tatt fra teori.pdf for lab 2)

h = 200 # horisontal avstand mellom yfast
xfast = np.asarray([0,h,2*h,3*h,4*h,5*h,6*h,7*h])
yfast = np.asarray([0.291, 0.248, 0.179, 0.135, 0.12, 0.126, 0.089, 0.016])
xfast = xfast/1000 # Omgjør fra mm til m

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

# Farten
vy = []
for i in range(len(y)):
    vy.append((abs(( (2*g) * (y[0] - y[i]) ) / (1 + c1)))**(0.5))

# Krumningsradius, obviosly
krumningsRadius = []
for i in range(0, len(d2y)):
    krumningsRadius.append(((d2y[i]) / (1+(dy[i])**2)**(1.5)))

# Sentripitalakselerasjon
a = []
for i in range(len(vy)):
    a.append((vy[i]**2) * krumningsRadius[i])

# Beta
beta = []
for i in dy:
    beta.append(np.arctan(i))

# Normalkraften, obviously
normalkraft = []
for i in range(0, len(beta)):
    normalkraft.append(M*(g*np.cos(beta[i]) + a[i]))

# Friksjonskraft, obviously
friksjonskraft = []
for i in range(0, len(normalkraft)):
    friksjonskraft.append((c1*M*g*np.sin(beta[i]))/(1+c1))

# Forholdet mellom friksjonskraften og normalkraften
forholdFogN = []
for i in range (len(normalkraft)):
    forholdFogN.append(abs(friksjonskraft[i] / normalkraft[i]))

# Plot
baneform = plt.figure('f/n',figsize=(12,6))
plt.plot(x,forholdFogN,xfast,yfast," ")
plt.title('f/n')
plt.xlabel('x(m)',fontsize=12)  
plt.ylabel('|f/n|',fontsize=12)
plt.ylim(-0.010,0.15)
plt.grid()
plt.show()
