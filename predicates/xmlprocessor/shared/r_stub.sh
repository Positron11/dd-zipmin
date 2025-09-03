#!/usr/bin/env bash
set -Eeuo pipefail

print_usage() {
  printf >&2 "Usage: $(basename $0) [--good-port PORT] [--input NAME] [-h|--help]

Options:
  --good-port PORT   Port to start on (default: 1984)
  --input NAME       Input filename or relative path to use (default: input.xml)
  -h, --help         Show this help and exit"
}

SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" >/dev/null 2>&1 && pwd)"
TEMPLATE="${SCRIPT_DIR}/../shared/r_base.sh"

BASEX_GOOD_PORT=1984
INPUT_NAME=input.xml

while [[ $# -gt 0 ]]; do
	case "$1" in
		--good-port)
	  		if [[ -n "$2" && "$2" =~ ^[0-9]+$ ]]; then
				BASEX_GOOD_PORT="$2"; shift 2
	  		else
				echo "Error: --good-port requires a numeric argument" >&2
				exit 2
	  		fi ;;
	
		--input)
			if [[ -n "${2:-}" && "$2" != /* && ! $2 =~ ^- ]]; then
				INPUT_NAME="$2"; shift 2
			else
				echo "Error: --input requires a relative path" >&2
				exit 2
			fi ;;
		
		 -h|--help) print_usage ; exit 0 ;;
		
		*)
			echo "Unknown option: $1" >&2
			print_usage
			exit 2 ;;
	esac
done

# source GOOD_VERSION and BAD_VERSION from v.sh in this directory
if [[ -f "$SCRIPT_DIR/v.sh" ]]; then
	source "$SCRIPT_DIR/v.sh"
else
	echo "Missing v.sh next to r.sh (expected GOOD_VERSION BAD_VERSION)" >&2
	exit 2
fi

export GOOD_VERSION BAD_VERSION

# Forward the optional good-port and input filename to the template.
exec bash "$TEMPLATE" "$SCRIPT_DIR" "$BASEX_GOOD_PORT" "$INPUT_NAME"
