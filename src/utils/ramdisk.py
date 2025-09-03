from pathlib import Path
import tempfile
import shutil


class RamdiskUnavailable(RuntimeError):
	def __init__(self, ram_root:Path):
		self.ram_root = ram_root

		super().__init__(f"RAM-disk unavailable at {self.ram_root}")


class RamDir():
	def __init__(self, prefix:str, ram_root:Path=Path("/dev/shm")):
		# cannot resolve RAM-disk path
		if not ram_root.exists() or not ram_root.is_dir(): raise RamdiskUnavailable(ram_root)
		
		self.prefix   = prefix
		self.ram_root = ram_root
		self.ram_dir  = Path(tempfile.mkdtemp(prefix=f"{self.prefix}-", dir=str(self.ram_root)))


	def __str__(self):
		return str(self.ram_dir)


	def copy(self, dir_map:list[tuple[Path, str]]) -> None:
		"""Copy directories to RAM-disk directory."""

		# copy directories
		for (source, dest) in dir_map:
			shutil.copytree(source, self.ram_dir / dest)


	def clean(self) -> None:
		try: shutil.rmtree(self.ram_dir)
		except Exception as e: print(f"Warning: failed to clean ramdisk dir: {e}", file=sys.stderr)