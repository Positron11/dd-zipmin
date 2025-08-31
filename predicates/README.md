# Predicates

Real-world predicates (reproducers) used to exercise the Delta‑Debugging algorithms in this repo. A predicate is a command/script that returns exit code 0 when a given input is “interesting” (e.g., reproduces a bug), and non‑zero otherwise. The minimizers call predicates repeatedly while shrinking inputs.

## Layout

- `xmlprocessor/`: XQuery differential tests driven by `r.sh` in each case directory. Uses a shared `lib/` with required jars.
<!-- - `ccompiler/`: Compiler-based predicates (e.g., GCC/Clang cases) following the same `r.sh` pattern.
- `unixtool/`: Predicates for Unix command-line tools. -->

## Credits

These predicates were originally sourced from the [artifact](https://zenodo.org/records/14854239) for “Toward a Better Understanding of Probabilistic Delta Debugging” (Zhang et al.); slight modifications were made to suit this work’s use case.
