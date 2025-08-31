from typing import Callable
from datetime import datetime


def complement_sweep(target:str, partlen:int, oracle:Callable) -> str:
	"""Identify benign chunks of target with variable granularity."""

	reduced = ""
	
	for i in range(0, len(target), partlen):
		removed   = target[i:i+partlen]
		remaining = target[i+partlen:]
		
		if not oracle(reduced + remaining): reduced += removed
	
	return reduced


def minimize(target:str, oracle:Callable, verbose:bool=False) -> str:
	"""Classical Delta-Debugging algorithm."""

	partlen = len(target) // 2
	
	while partlen and target:
		if verbose: print(f"[{datetime.now().strftime("%H:%M:%S")}]  {len(target):.2E}  {partlen}")

		reduced = complement_sweep(target, partlen, oracle)
		
		if reduced == target: partlen //= 2		
		target = reduced
	
	return target
