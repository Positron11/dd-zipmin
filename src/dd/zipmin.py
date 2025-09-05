from typing import Callable
from math import ceil
from datetime import datetime


def remove_last_char(pre:str, target:str, post:str, oracle:Callable) -> tuple[str, str, str]:
	"""Add last char to postlude if needed."""

	interesting, wellformed = oracle(pre + target[:-1] + post)

	if interesting: return pre, target[:-1], post, wellformed
	else: return pre, target[:-1], target[-1] + post, wellformed


def complement_sweep(pre:str, target:str, post:str, partlen:int, oracle:Callable) -> tuple[str, int]:
	"""Identify benign chunks of target with variable granularity."""
	
	n_good_oracalls = 0

	reduced = ""
	
	# test contiguous chunks of size partlen for interestingness
	for i in range(0, len(target), partlen):
		removed   = target[i:i+partlen]
		remaining = target[i+partlen:]
		
		interesting, wellformed = oracle(pre + reduced + remaining + post)

		if wellformed: n_good_oracalls += 1

		if not interesting: reduced += removed
	
	n_oracalls = ceil(len(target) / partlen)
	deficit    = max(n_oracalls - (len(target) - len(reduced)), 0)
	
	return reduced, deficit, n_good_oracalls


def minimize(target:str, oracle:Callable, stats:bool=False, verbose:bool=False) -> tuple[str, int]|str:
	"""ZipMin Delta-Debugging aglorithm."""

	partlen = len(target) // 2
	
	# counters
	c_iteralt  = 0
	deficit    = 0
	n_oracalls = 0
	n_good_oracalls = 0
	
	# pre and post-ludes
	pre  = ""
	post = ""
	
	# alternate between deficit-guided last char trimming and complement sweep
	while partlen and target:
		if verbose: print(f"[{datetime.now().strftime("%H:%M:%S")}]  {len(pre + target + post):.2E}  {partlen}")

		if c_iteralt % 2: 
			for i in range(deficit):
				pre, target, post, wellformed = remove_last_char(pre, target, post, oracle)

				if stats and wellformed: n_good_oracalls += 1

			if stats: n_oracalls += deficit
			  
			deficit = 0
		
		else:
			reduced, deficit, n_sweep_good_oracalls = complement_sweep(pre, target, post, partlen, oracle)
			
			if stats: n_oracalls += ceil(len(target) / partlen)
			if stats: n_good_oracalls += n_sweep_good_oracalls
	
			if reduced == target: partlen //= 2
		
			target = reduced
		
		c_iteralt += 1
	
	return (pre + target + post, n_oracalls, n_good_oracalls) if stats else pre + target + post
