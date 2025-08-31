from typing import Callable
from math import ceil
from datetime import datetime


def complement_sweep(target:str, partlen:int, oracle:Callable) -> str:
	"""Identify benign chunks of target with variable granularity."""

	reduced = ""
	
	# test contiguous chunks of size partlen for interestingness
	for i in range(0, len(target), partlen):
		removed   = target[i:i+partlen]
		remaining = target[i+partlen:]
		
		if not oracle(reduced + remaining): reduced += removed
	
	return reduced


def minimize(target:str, oracle:Callable, stats:bool=False, verbose:bool=False) -> tuple[str, int]|str:
	"""Classical Delta-Debugging algorithm."""

	# count total oracle calls
	n_oracalls = 0

	partlen = len(target) // 2
	
	while partlen and target:
		if verbose: print(f"[{datetime.now().strftime("%H:%M:%S")}]  {len(target):.2E}  {partlen}")

		reduced = complement_sweep(target, partlen, oracle)
		if stats: n_oracalls += ceil(len(target) / partlen)
		
		if reduced == target: partlen //= 2		
		
		target = reduced
	
	return (target, n_oracalls) if stats else target
