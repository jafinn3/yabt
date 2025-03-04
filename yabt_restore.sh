#!/bin/bash

set -e  # Exit on error

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -t|--timestamp) TIMESTAMP="$2"; shift 2 ;;
        -y|--yabt_dir) YABT_DIR="$2"; shift 2 ;;
        -r|--restore_dir) RESTORE_DIR="$2"; shift 2 ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
done

if [[ ! -d "$YABT_DIR" ]]; then
    echo "Error: yabt directory does not exist."
    exit 1
fi

mkdir -p "$RESTORE_DIR"

YABT_PATH="$YABT_DIR/$TIMESTAMP"
if [[ ! -d "$YABT_PATH" ]]; then
    echo "Error: yabt directory for timestamp '$TIMESTAMP' does not exist."
    exit 1
fi

echo "Restoring backup from '$YABT_PATH' to '$RESTORE_DIR'..."

cp -a "$YABT_PATH/." "$RESTORE_DIR/"

echo "Restore complete."

