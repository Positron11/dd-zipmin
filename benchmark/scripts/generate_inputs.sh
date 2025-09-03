#!/usr/bin/env bash
set -euo pipefail

# minimal: run cherry_pick 5 times per case via basexserver_wrapper

SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" >/dev/null 2>&1 && pwd)"

for case in 3 4 5; do
	CASE_DIR="${SCRIPT_DIR}/../../predicates/xmlprocessor/xml-1e9bc83-${case}"
	
	mkdir -p "$CASE_DIR/input.pick"

	for i in {1..5}; do
		echo "[case $case] run $i -> $CASE_DIR/input.pick/$i.xml"
		
		$SCRIPT_DIR/../../scripts/basexserver_wrapper -- \
			$SCRIPT_DIR/../../scripts/cherry_pick \
			--ramdisk \
			--max-kb $((5 + $case)) \
			"$CASE_DIR/" \
			--output "input.pick/$i.xml"
	done
done

echo "Done."
