import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline

"""
Denne modulen utgjør omtrent havlparten av arbeidet i lab 2.
Modulen inkluderer metoder for beregne og plotte sentrale verdier som: 
- krumningsradius
- fart
- sentripitalakselerasjon
- betavinkel
- normalkraft

Plotting av ønsket metode gjøres på kodelinje 105.
"""

# Globale konstanter:
g = -9.81 # Gravitasjonskonstanten
M = 0.030 # Massen til objektet vi skal bruke i forsøket
c1 = 0.5 # C for den kompakte skiva (tatt fra teori.pdf for lab 2)

# Sentrale tall for banen vår
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


#--------------------------------- METODER ---------------------------------#

def krumningsradius():
    """
    Metoden finner krumninsradiusen til objektet vårt
    """
    krum = []
    for i in range(0, len(d2y)):
        krum.append((d2y[i]) / (1+(dy[i])**2)**(1.5))
    return krum

def velocity(c):
    """
    Metoden finner farten til objektet vårt
    """
    vy = []
    for i in range(len(y)):
        vy.append((abs(( (2*g) * (y[0] - y[i]) ) / (1 + c)))**(0.5))
    return vy

def sentAcc(c):
    """
    Metoden finner sentripitalakselerasjonen
    """
    vy = velocity(c)
    krumRad = krumningsradius()
    a = []
    for i in range(len(vy)):
        a.append((vy[i]**2) * krumRad[i])
    return a

def betaRadians():
    """
    Metoden finner betavinkelen
    """
    # Beta
    beta = []
    for i in dy:
        beta.append(np.arctan(i))
    return beta

def normalForce(c):
    """
    Metoden finner normalkraften
    """
    # Normalkraften, obviously
    a = sentAcc(c)
    beta = betaRadians()
    normalkraft = []
    for i in range(0, len(beta)):
        normalkraft.append(M*(g*np.cos(beta[i]) + a[i]))
    return normalkraft

def friksjonskraft(c):
    friksjon = []
    normalkraft = normalForce(c)
    beta = betaRadians()
    for i in range(0, len(normalkraft)):
        friksjon.append((c*M*g*np.sin(beta[i]))/(1+c))
    return friksjon

def friksjonDeltPåNormalkraft(c):
    """
    Metoden finner forholdet mellom friksjonskraften og normalkraften
    """
    forholdFogN = []
    normalkraft = normalForce(c)
    friksjon = friksjonskraft(c)
    for i in range (len(normalkraft)):
        forholdFogN.append(abs(friksjon[i] / normalkraft[i]))
    return forholdFogN

def plotting(y_axis):
    """
    Metoden plotter ønsket metode
    """
    # Plot
    baneform = plt.figure('f/n',figsize=(12,6))
    plt.plot(x,y_axis,xfast,yfast," ")
    plt.title('f/n')
    plt.xlabel('x(m)',fontsize=12)  
    plt.ylabel('|f/n|',fontsize=12)
    #plt.ylim(-1.7, 1.2)
    plt.grid()
    plt.show()

# Kall for å plotte ønkset metode:
plotting(friksjonDeltPåNormalkraft(c1))