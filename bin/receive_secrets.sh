#!/usr/bin/env sh

LOGIN_CHECK="$(bw login --check | grep 'You are logged in!')"
if [ -z "$LOGIN_CHECK" ]; then
  echo ""
else
  export BW_SESSION=$(bw login --raw)
fi

FOLDER_ID=$(bw get folder ${1} | jq -r .id)

JSONATA_FILTER='$map($, function($v) {
    $lowercase($v.name) & ": " & $v.login.password
})'

bw list items --folderid $FOLDER_ID | jfq "$JSONATA_FILTER"
