from typing import Callable


def complement_sweep(target:str, i_partition:int, oracle:Callable):
	"""Identify benign chunks of target with variable granularity."""

	reduced = ""
	
	for i in range(0, len(target), i_partition):
		stitched = reduced + target[i+i_partition:]
		
		if not oracle(stitched): reduced += target[i:i+i_partition]
	
	return reduced


def ddmin(target:str, oracle:Callable) -> str:
	"""Classical Delta-Debugging algorithm."""

	i_partition = len(target) // 2
	
	while i_partition and target:
		reduced = complement_sweep(target, i_partition, oracle)
		
		if reduced == target: i_partition //= 2		
		target = reduced
	
	return target