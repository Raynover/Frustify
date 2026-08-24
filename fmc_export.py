from pathlib import Path
from typing import TextIO

ROOT_DIR = Path(__file__).resolve().parent
FMC_STRUCTURE_DIR = ROOT_DIR / "fmc_structure"
OUTPUT_DIR = ROOT_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def gets_output_filepath(filename: str) -> Path:
    """Combines the output directory path with the given filename."""
    return OUTPUT_DIR / filename
    
def gets_structure_filepath(filename: str) -> Path:
    """Combines the fmc_structure directory path with the given filename."""
    return OUTPUT_DIR / filename


# check this! for the end of fmc. Maybe it can be dealt in another way
def appends_break_line_char(file_handle: TextIO) -> None:
    """Writes a newline character to an open file stream."""
    file_handle.write("\n")
    
def writes_preamble(file_handle: TextIO) -> None:
	"""Copies preamble.txt into the open file stream."""
	preamble_path = FMC_STRUCTURE_DIR / "preamble.txt"
	content = preamble_path.read_text(encoding="utf-8")
	file_handle.write(content)
	
def appends_scroll_out(file_handle: TextIO) -> None:
	"""Copies scroll_out.txt into the open file stream."""
	scroll_path = FMC_STRUCTURE_DIR / "scroll_out.txt"
	content = scroll_path.read_text(encoding="utf-8")
	file_handle.write("\n" + content)
	
def appends_richiamo_fresa(file_handle: TextIO, spx: float, spy: float, is_inner: bool) -> None:
	""" Reads richiamo_fresa.txt template, formats coordinates, and writes to stream. """
	fresa_path = FMC_STRUCTURE_DIR / "richiamo_fresa.txt"
	content = fresa_path.read_text(encoding="utf-8")
	if is_inner == True:
		lgean = 50
	else:
		lgean = 200	
	formatted_block = content.format(spx=spx, spy=spy, lgean=lgean)
	file_handle.write("\n" + formatted_block)

def appends_circle_clockwise(file_handle: TextIO, epx: float, epy: float, aktina: float) -> None:
	""" Reads circle_clockwise.txt template, formats coordinates, and writes to stream. """
	clockwise_path = FMC_STRUCTURE_DIR / "circle_clockwise.txt"
	content = clockwise_path.read_text(encoding="utf-8")
	formatted_block = content.format(epx=epx, epy=epy, aktina=aktina)
	file_handle.write("\n" + formatted_block)

def appends_straight_line(file_handle: TextIO, epx: float, epy: float) -> None:
	""" Reads straight_line.txt template, formats coordinates, and writes to stream. """
	line_path = FMC_STRUCTURE_DIR / "straight_line.txt"
	content = line_path.read_text(encoding="utf-8")
	formatted_block = content.format(epx=epx, epy=epy)
	file_handle.write("\n" + formatted_block)

def appends_circle_anticlockwise(file_handle: TextIO, epx: float, epy: float, aktina: float) -> None:
	""" Reads circle_anticlockwise.txt template, formats coordinates, and writes to stream. """
	anticlockwise_path = FMC_STRUCTURE_DIR / "circle_anticlockwise.txt"
	content = anticlockwise_path.read_text(encoding="utf-8")
	formatted_block = content.format(epx=epx, epy=epy, aktina=aktina)
	file_handle.write("\n" + formatted_block)

def appends_scanalatura(file_handle: TextIO, spx: float, spy: float, epx: float, epy: float) -> None:
	""" Reads scanalatura.txt template, formats coordinates, and writes to stream. """
	scanalatura_path = FMC_STRUCTURE_DIR / "scanalatura.txt"
	content = scanalatura_path.read_text(encoding="utf-8")
	formatted_block = content.format(spx=spx, spy=spy, epx=epx, epy=epy)
	file_handle.write("\n" + formatted_block)
