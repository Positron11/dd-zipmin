from typing import Callable
from math import ceil
from datetime import datetime


def remove_last_char(pre:str, target:str, post:str, oracle:Callable) -> tuple[str, str, str]:
	"""Add last char to postlude if needed."""

	if oracle(pre + target[:-1] + post): return pre, target[:-1], post
	else: return pre, target[:-1], target[-1] + post


def complement_sweep(pre:str, target:str, post:str, partlen:int, oracle:Callable) -> tuple[str, int]:
	"""Identify benign chunks of target with variable granularity."""
	
	reduced = ""
	
	# test contiguous chunks of size partlen for interestingness
	for i in range(0, len(target), partlen):
		removed   = target[i:i+partlen]
		remaining = target[i+partlen:]
		
		if not oracle(pre + reduced + remaining + post): reduced += removed
	
	n_oracalls = ceil(len(target) / partlen)
	deficit    = max(n_oracalls - (len(target) - len(reduced)), 0)
	
	return reduced, deficit


def minimize(target:str, oracle:Callable, stats:bool=False, verbose:bool=False) -> tuple[str, int]|str:
	"""ZipMin Delta-Debugging aglorithm."""

	partlen = len(target) // 2
	
	# counters
	c_iteralt  = 0
	deficit    = 0
	n_oracalls = 0
	
	# pre and post-ludes
	pre  = ""
	post = ""
	
	# alternate between deficit-guided last char trimming and complement sweep
	while partlen and target:
		if verbose: print(f"[{datetime.now().strftime("%H:%M:%S")}]  {len(pre + target + post):.2E}  {partlen}")

		if c_iteralt % 2: 
			for i in range(deficit):
				pre, target, post = remove_last_char(pre, target, post, oracle)

			if stats: n_oracalls += deficit
			  
			deficit = 0
		
		else:
			reduced, deficit = complement_sweep(pre, target, post, partlen, oracle)
			if stats: n_oracalls += ceil(len(target) / partlen)
	
			if reduced == target: partlen //= 2
		
			target = reduced
		
		c_iteralt += 1
	
	return (pre + target + post, n_oracalls) if stats else pre + target + post
