import math
import numpy as np
from typing import TextIO
import fmc_export as fmc
import parameters as prm


def calculate_kerf_coordinates(file_handle: TextIO):
	""" Writes the fmc part for the kerfs with the disc """
	
	n = math.floor( ( prm.S - prm.leftoffset ) / prm.d )
	d_adjusted = ( prm.S - prm.leftoffset ) / n
	n = math.floor( ( prm.S - prm.leftoffset ) / d_adjusted )
	theta = d_adjusted / prm.L0mikro

	for k in range( 1 , n + 1 ):
		spx = ( prm.L0mikro - prm.discroom ) * np.cos( k * theta + prm.peristrofh) - prm.xtrl
		spy = ( prm.L0mikro - prm.discroom ) * np.sin( k * theta + prm.peristrofh) - prm.ytrl
		epx = ( prm.L0megalo + prm.discroom ) * np.cos( k * theta + prm.peristrofh) - prm.xtrl
		epy = ( prm.L0megalo + prm.discroom ) * np.sin( k * theta + prm.peristrofh) - prm.ytrl
		fmc.appends_scanalatura(file_handle, spx, spy, epx, epy)
