import time
import math
import numpy as np
import parameters as prm
import helper_translate as trl
import fmc_export as fmc
import write_outline as wln
import write_kerfs as wkr


def main():
	
	start_time = time.perf_counter()
		
	output_path = fmc.gets_output_filepath("output.fmc")
	
	with open(output_path, "w", encoding="utf-8") as f:
		fmc.writes_preamble(f)
		wln.calculate_arc_of_circ_ring(f)
		wkr.calculate_kerf_coordinates(f)
		fmc.appends_break_line_char(f)
	
	print("Your scripts are ready in the output folder!")
	end_time = time.perf_counter()
	elapsed_time = end_time - start_time
	print(f"Execution time was {elapsed_time:.4f} seconds.")
	

if __name__ == "__main__":
	main()
