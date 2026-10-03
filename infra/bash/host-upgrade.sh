#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "usage: $0 user@host [debian|ubuntu|fedora]" >&2
  exit 1
}

[[ $# -ge 1 ]] || usage
TARGET="$1"
FAMILY="${2:-}"

ssh_cmd() {
  ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new "$TARGET" "$@"
}

if [[ -z "$FAMILY" ]]; then
  FAMILY="$(ssh_cmd '. /etc/os-release; echo "$ID"')"
fi

case "$FAMILY" in
  debian)
    ssh_cmd 'sudo apt-get update && sudo DEBIAN_FRONTEND=noninteractive apt-get -y dist-upgrade'
    ;;
  ubuntu)
    ssh_cmd 'sudo apt-get update && sudo DEBIAN_FRONTEND=noninteractive apt-get -y dist-upgrade'
    ;;
  fedora)
    ssh_cmd 'sudo dnf -y upgrade'
    ;;
  *)
    echo "unsupported family: $FAMILY" >&2
    exit 1
    ;;
esac
