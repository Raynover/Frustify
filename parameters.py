import math
import numpy as np
import helper_translate as trl

# Constants
R = 493.0
r = 217.0
h = 710.0

# Direct Results
littleh = r * h / ( R - r )
bigh = littleh + h

L0mikro = np.sqrt( littleh ** 2 + r ** 2 )
L0megalo = np.sqrt( bigh ** 2 + R ** 2 )

S = 2 * math.pi * r
gwnia = S / L0mikro
peristrofh = ( math.pi - gwnia ) / 2

# Specs
d = 8
discwidth = 3.0
leftoffset = d - discwidth
discroom = 10 # Gives room for disc to start cutting outside the wood - so it won't damage it

moires = 0.5
phi = math.pi * moires / 180
accuracy = 360 / moires


# Coordinates of outline points (see reference drawing files in the readme/ folder), after retrieving translations
xtrl, ytrl = trl.calculates_translations()
xA = L0mikro * np.cos( gwnia + peristrofh ) - xtrl
yA = L0mikro * np.sin( gwnia + peristrofh ) - ytrl
xM = L0mikro * np.cos( gwnia / 2 + peristrofh ) - xtrl
yM = L0mikro * np.sin( gwnia / 2 + peristrofh ) - ytrl
xB = - L0mikro * np.cos( gwnia + peristrofh ) - xtrl
yB = L0mikro * np.sin( gwnia + peristrofh ) - ytrl
xC = - L0megalo * np.cos( gwnia + peristrofh ) - xtrl
yC = L0megalo * np.sin( gwnia + peristrofh ) - ytrl
xN = L0megalo * np.cos( gwnia / 2 + peristrofh ) - xtrl
yN = L0megalo * np.sin( gwnia / 2 + peristrofh ) - ytrl
xD = L0megalo * np.cos( gwnia + peristrofh ) - xtrl
yD = L0megalo * np.sin( gwnia + peristrofh ) - ytrl
