from typing import TextIO
import parameters as prm
import fmc_export as fmc


def calculate_arc_of_circ_ring(file_handle: TextIO):
	""" Writes the fmc part for the outline cut with the end mill """
		
	fmc.appends_richiamo_fresa(file_handle, prm.xA, prm.yA, True)
	
	fmc.appends_circle_clockwise(file_handle, prm.xM, prm.yM, prm.L0mikro)
	
	fmc.appends_circle_clockwise(file_handle, prm.xB, prm.yB, prm.L0mikro)
	
	fmc.appends_straight_line(file_handle, prm.xC, prm.yC)
	
	fmc.appends_circle_anticlockwise(file_handle, prm.xN, prm.yN, prm.L0megalo)
	
	fmc.appends_circle_anticlockwise(file_handle, prm.xD, prm.yD, prm.L0megalo)
	
	fmc.appends_straight_line(file_handle, prm.xA, prm.yA)
	
	fmc.appends_scroll_out(file_handle)
	
	fmc.appends_richiamo_fresa(file_handle, prm.xC, prm.yC, False)
	
	fmc.appends_circle_anticlockwise(file_handle, prm.xN, prm.yN, prm.L0megalo)
	
	fmc.appends_circle_anticlockwise(file_handle, prm.xD, prm.yD, prm.L0megalo)
	
	fmc.appends_scroll_out(file_handle)
