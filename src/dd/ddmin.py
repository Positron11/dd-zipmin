from typing import Callable
from math import ceil
from datetime import datetime


def complement_sweep(target:str, partlen:int, oracle:Callable) -> str:
	"""Identify benign chunks of target with variable granularity."""

	n_good_oracalls = 0

	reduced = ""
	
	# test contiguous chunks of size partlen for interestingness
	for i in range(0, len(target), partlen):
		removed   = target[i:i+partlen]
		remaining = target[i+partlen:]
		
		interesting, wellformed = oracle(reduced + remaining)

		if wellformed: n_good_oracalls += 1

		if not interesting: reduced += removed
	
	return reduced, n_good_oracalls


def minimize(target:str, oracle:Callable, stats:bool=False, verbose:bool=False) -> tuple[str, int]|str:
	"""Classical Delta-Debugging algorithm."""

	# count total oracle calls
	n_oracalls = 0
	n_good_oracalls = 0

	partlen = len(target) // 2
	
	while partlen and target:
		if verbose: print(f"[{datetime.now().strftime("%H:%M:%S")}]  {len(target):.2E}  {partlen}")

		reduced, n_sweep_good_oracalls = complement_sweep(target, partlen, oracle)
		
		if stats: n_oracalls += ceil(len(target) / partlen)
		if stats: n_good_oracalls += n_sweep_good_oracalls
		
		if reduced == target: partlen //= 2		
		
		target = reduced
	
	return (target, n_oracalls, n_good_oracalls) if stats else target
