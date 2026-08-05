#!/usr/bin/env sh

# SPDX-FileCopyrightText: 2026 2026 Oliver Lorenz
#
# SPDX-License-Identifier: AGPL-3.0-or-later

MODE="$1"

if [ "$MODE" != "folder" ] && [ "$MODE" != "collection" ] || [ $# -lt 2 ]; then
  echo "Usage: $0 <folder|collection> <hostname> [hostname...]" >&2
  exit 1
fi

shift

LOGIN_CHECK="$(bw login --check | grep 'You are logged in!')"
if [ -z "$LOGIN_CHECK" ]; then
  echo ""
else
  export BW_SESSION=$(bw login --raw)
fi

JSONATA_FILTER='$map($, function($v) {
    $lowercase($v.name) & ": " & $v.login.password
})'

for MASH_HOSTNAME in "$@"; do
  ITEM_ID=$(bw get "$MODE" "$MASH_HOSTNAME" | jq -r .id)

  if [ -z "$ITEM_ID" ] || [ "$ITEM_ID" = "null" ]; then
    echo "No Bitwarden ${MODE} found for '${MASH_HOSTNAME}', skipping." >&2
    continue
  fi

  OUTPUT_DIR="inventory/host_vars/${MASH_HOSTNAME}"
  mkdir -p "$OUTPUT_DIR"

  bw list items --"${MODE}id" "$ITEM_ID" | jfq "$JSONATA_FILTER" > "${OUTPUT_DIR}/secrets.yml"
  echo "Wrote ${OUTPUT_DIR}/secrets.yml"
done
