import math
import numpy as np
import parameters as prm

def calculates_translations():
	""" Calculates x and y translations to match CNC's origin """
	if prm.gwnia <= np.pi:
		xtrl = prm.L0megalo * np.cos( prm.gwnia + prm.peristrofh )
		ytrl = prm.L0mikro * np.sin( prm.gwnia + prm.peristrofh )
	else:
		xtrl = 0
		ytrl = 0
		Sphi = prm.phi * prm.R
		theta = np.arccos( 1 - Sphi ** 2 / ( 2 * prm.L0megalo ** 2 ) )
		for k in range( math.floor( prm.accuracy / 2 ) , math.floor( prm.accuracy ) + 1 ):
			if prm.L0megalo * np.cos( k * theta + prm.peristrofh ) < xtrl:
				xtrl = prm.L0megalo * np.cos( k * theta + prm.peristrofh )
			if prm.L0megalo * np.sin( k * theta + prm.peristrofh ) < ytrl:
				ytrl = prm.L0megalo * np.sin( k * theta + prm.peristrofh )
	return xtrl, ytrl
