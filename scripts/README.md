# Scripts

Helper commands to run and benchmark the XML delta‑debugging workflows in this repo. These are thin CLIs; core logic lives under `src/`.

## Prerequisites

- **Python 3.8+** and the package in editable mode, or set `PYTHONPATH=src`:

	- Recommended quick setup: 
	
		```Bash
		python -m venv .venv && source .venv/bin/activate && python -m pip install -U pip && python -m pip install -e .
		```

- **Java (JDK 11+)**. Used by Saxon and BaseX clients/servers.

- `nc`/`netcat` available on PATH.

- Predicate assets under `predicates/xmlprocessor/` (already included: Saxon JAR, BaseX JARs, shared scripts).

## Binaries

All binaries provide usage help via the `-h` flag.

- `scripts/basexserver_wrapper` (bash)
	- Starts a matching pair of BaseX servers (good/bad) on free contiguous ports.
	- Finds the nearest predicate dir (by locating a `v.sh` in subcommand args).
	- Exports the selected good port to the subcommand by appending `--good-port <PORT>`.
	- Cleans up servers on exit.

- `scripts/cherry_pick` (python)
	- Randomly removes XML element subtrees while the predicate stays “interesting” and size stays within bounds.
	- Typical flags: `--min-kb`, `--max-kb`, `--seed`, `--ramdisk`, `--output`, `--verbose`.

- `scripts/minimize_xml` (python)
	- Runs a minimization algorithm from a Python module (default `dd.ddmin`) against the predicate.
	- Typical flags: `--module`, `--ramdisk`, `--output`, `--verbose`.

## Tips

- **RAM‑disk:** Add `--ramdisk` to copy the predicate to `/dev/shm` for faster I/O. Output paths are still relative to the predicate dir.

- **Ports:** Without the wrapper, tools read `--good-port` (or `BASEX_GOOD_PORT`) to reach an already running BaseX “good” server. The wrapper handles port selection automatically.

- **Cleanups:** Tools restore `input.xml` after finishing and remove RAM‑disk copies when used.
