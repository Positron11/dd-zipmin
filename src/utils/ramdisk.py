from pathlib import Path
import tempfile
import shutil
import sys


class RamDiskUnavailable(RuntimeError):
	def __init__(self, ram_root:Path):
		self.ram_root = ram_root

		super().__init__(f"RAM-disk unavailable at {self.ram_root}")


class RamDir():
	"""RAM-disk temp. directory manager."""

	def __init__(self, prefix:str, root:Path=Path("/dev/shm")):
		if not root.exists() or not root.is_dir(): raise RamDiskUnavailable(root)
		
		self.prefix   = prefix
		self.root = root
		self.path  = Path(tempfile.mkdtemp(prefix=f"{self.prefix}-", dir=self.root))


	def __str__(self):
		return str(self.path)


	def copy(self, dir_map:list[tuple[Path, str]]) -> None:
		"""
		Copy file trees to RAM-disk directory.
		
		:param dir_map: map of source -> destination paths.
		"""

		# copy directories
		for (source, dest) in dir_map:
			shutil.copytree(source, self.path / dest)


	def clean(self) -> None:
		"""Remove directory from RAM-disk."""

		try: shutil.rmtree(self.path)
		except Exception as e: print(f"Warning: failed to clean ramdisk dir: {e}", file=sys.stderr)
