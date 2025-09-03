from __future__ import annotations

from typing import Callable
from pathlib import Path
from defusedxml import ElementTree as ET
import subprocess


EXIT_MESSAGES = {
	2: "Invalid option or bad arguments",
	3: "BaseX server not reachable",
	4: "BaseX .jar file not found",
}


def build_oracle(
	base:Path, 
	input_name:str, 
	script_name:str, 
	good_port:str|None, 
	timeout:float|None) -> Callable:
	
	"""Generate XML oracle callable for debugger."""

	xml_path    = base / input_name
	script_path = base / script_name
	
	cache: dict[str, bool] = {}

	def oracle(candidate:str) -> bool:
		# memoize repeated candidates across iterations
		hit = cache.get(candidate)
		if hit is not None: return hit

		# fast well-formedness pre-check
		try: ET.fromstring(candidate)
		
		except Exception: 
			cache[candidate] = False
			return False

		tmp_path = xml_path.with_suffix(xml_path.suffix + ".tmp")
		
		# write candidate to file and atomically replace
		tmp_path.write_text(candidate, encoding="utf-8")
		tmp_path.replace(xml_path)
		
		try:
			# pass good port to r.sh
			cmd = ["bash", str(script_path)]
			if good_port: cmd += ["--good-port", str(good_port)]
			
			# forward input file name to predicate template
			cmd += ["--input", input_name]
			
			proc = subprocess.run(cmd,
				cwd    =str(base),
				stdout =subprocess.DEVNULL,
				stderr =subprocess.DEVNULL,
				timeout=timeout,
				check  =False
			)

		# false on timeout
		except subprocess.TimeoutExpired:
			cache[candidate] = False
			return False

		# handle breaking errors
		if proc.returncode > 1: 
			print(f"Fatal Error ({proc.returncode}): {EXIT_MESSAGES.get(proc.returncode, 'Unknown')}")

			raise SystemExit(proc.returncode)

		# ok if desired error (retcode=0)
		ok = proc.returncode == 0
		
		cache[candidate] = ok
		return ok

	return oracle
