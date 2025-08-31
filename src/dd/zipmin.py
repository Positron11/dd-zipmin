from typing import Callable
from datetime import datetime


def remove_last_char(pre:str, target:str, post:str, oracle:Callable) -> tuple[str, str, str]:
	"""Add last char to postlude if needed."""

	if oracle(pre + target[:-1] + post): return pre, target[:-1], post
	else: return pre, target[:-1], target[-1] + post


def complement_sweep(pre:str, target:str, post:str, partlen:int, oracle:Callable) -> tuple[str, int]:
	"""Identify benign chunks of target with variable granularity."""
	
	reduced = ""
	
	failure_count = 0
	
	for i in range(0, len(target), partlen):
		removed   = target[i:i+partlen]
		remaining = target[i+partlen:]
		
		if not oracle(pre + reduced + remaining + post): reduced += removed
	
		else: failure_count += 1
	
	deficit = max(failure_count - (len(target) - len(reduced)), 0)
	
	return reduced, deficit


def minimize(target:str, oracle:Callable, verbose:bool=False) -> str:
	"""ZipMin Delta-Debugging aglorithm."""

	partlen = len(target) // 2
	
	# counters
	count   = 0
	deficit = 0
	
	# pre and post-ludes
	pre  = ""
	post = ""
	
	# alternate between deficit-guided last char trimming and complement sweep
	while partlen and target:
		if verbose: print(f"[{datetime.now().strftime("%H:%M:%S")}]  {len(target):.2E}  {partlen}")

		if count % 2: 
			for i in range(deficit):
				pre, reduced, post = remove_last_char(pre, target, post, oracle)
			  
			deficit = 0
		
		else:
			reduced, deficit = complement_sweep(pre, target, post, partlen, oracle)
	
			if reduced == target: partlen //= 2
		
		target = reduced
		count += 1
	
	return pre + target + post
