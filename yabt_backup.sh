#!/bin/bash

set -e  # Exit on error

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -s|--source_dir) SOURCE_DIR="$2"; shift 2 ;;
        -y|--yabt_dir) BACKUP_DIR="$2"; shift 2 ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
done

if [[ ! -d "$BACKUP_DIR" ]]; then
    echo "Error: Backup directory does not exist."
    exit 1
fi

LATEST_BACKUP=$(ls -d "$BACKUP_DIR"/*/ 2>/dev/null | sort | tail -n 1)

NEW_BACKUP="$BACKUP_DIR/$(date +%Y-%m-%d_%H-%M)"
mkdir -p "$NEW_BACKUP"

if [[ -n "$LATEST_BACKUP" ]]; then
    rsync -a --link-dest="$LATEST_BACKUP" "$SOURCE_DIR/" "$NEW_BACKUP/"
else
    rsync -a "$SOURCE_DIR/" "$NEW_BACKUP/"
fi

echo "Backup created: $NEW_BACKUP"

