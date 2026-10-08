#!/bin/sh
# Example: mirror the pod to an external drive, skipping the plain-text sensitive/ folder and secrets.
# Usage: POD_DIR=~/context-pod BACKUP_DIR=/path/to/drive/pod-backup sh system/backup.sh
# The drive itself should be encrypted. The sensitive layer travels as sensitive.tar.gz.age.
set -eu

POD_DIR="${POD_DIR:-$HOME/context-pod}"
BACKUP_DIR="${BACKUP_DIR:?set BACKUP_DIR to a folder on your backup drive}"

if [ ! -d "$(dirname "$BACKUP_DIR")" ]; then
  echo "backup drive not mounted ($(dirname "$BACKUP_DIR")); skipping" >&2
  exit 0
fi

mkdir -p "$BACKUP_DIR"
rsync -a --delete \
  --exclude '/sensitive/' \
  --exclude '*.key' --exclude '.env' --exclude '.env.*' --exclude 'packs/' \
  "$POD_DIR"/ "$BACKUP_DIR"/
echo "backed up $POD_DIR -> $BACKUP_DIR at $(date '+%Y-%m-%d %H:%M')"
