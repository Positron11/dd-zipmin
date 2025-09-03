# Predicates

Real-world predicates (reproducers) used to exercise the Delta‑Debugging algorithms in this repo. A predicate is a command/script that returns exit code 0 when a given input is “interesting” (e.g., reproduces a bug), and non‑zero otherwise. The minimizers call predicates repeatedly while shrinking inputs.

The original inputs (see [Credits](#credits)) were stochastically pre-shrunk (see [cherry_pick](../scripts/README.md/#scripts)), being designed for benchmarking with HDD - benchmarking byte-by-byte DD with ~100kb inputs proved infeasible for execution time.

## Predicate Layout (xmlprocessor)

Each test case directory (e.g. `predicates/xmlprocessor/xml-1e9bc83-3/`) contains:

- `input.xml`: Original source XML for the predicate
- `input.pick/<i>.xml`: Stochastically reduced input XML (actual test case)
- `query.xq`: XQuery used by Saxon/BaseX
- `r.sh`: Runner (symlink to `shared/r_stub.sh`)
- `v.sh`: Defines `GOOD_VERSION` and `BAD_VERSION` BaseX JAR tags

### Shared Resources

- `../lib/`: Saxon and BaseX JARs
- `../shared/`: Common runner templates

## Credits

These predicates were originally sourced from the [artifact](https://zenodo.org/records/14854239) for “Toward a Better Understanding of Probabilistic Delta Debugging” (Zhang et al.); slight modifications were made to suit this work’s use case.
