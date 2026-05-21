#!/usr/bin/env bash

# SPDX-FileCopyrightText: 2026 2026 Oliver Lorenz
#
# SPDX-License-Identifier: AGPL-3.0-or-later

set -e
if [ ! -f .env-init ]; then
  echo "ERROR: .env-init file not found"
  exit 1
fi

source .env-init

ENV_VARS_LIST=$(grep -Eo ROLE_[A-Z0-9_]+ .env-init | uniq)
HAS_ERRORS=0
for ENV_VAR in $ENV_VARS_LIST; do
  if [ -z "${!ENV_VAR}" ]; then echo "ERROR: $ENV_VAR is not set"; HAS_ERRORS=1; fi
done

if [ $HAS_ERRORS -eq 1 ]; then
  echo "ERROR: Please set the missing environment variables in .env-init"
  exit 1
fi

echo "INFO:  All required environment variables are set."
if [ ! -z $DRY_RUN ]; then
  echo "INFO:  Dry run mode, no files will be changed."
fi

echo -e "\nINFO:  Renaming files ..."

for ENV_VAR in $ENV_VARS_LIST; do
  FILES_TO_RENAME_LIST=$(find . -depth -name "*<$ENV_VAR>*")
  for FILE_TO_RENAME in $FILES_TO_RENAME_LIST; do
    echo "INFO:  Renaming $FILE_TO_RENAME to ${FILE_TO_RENAME//<$ENV_VAR>/${!ENV_VAR}}"
    if [ -z "$DRY_RUN" ]; then
      mv "$FILE_TO_RENAME" "${FILE_TO_RENAME//<$ENV_VAR>/${!ENV_VAR}}"
    fi
  done
done

echo -e "\nINFO:  Replacing variables in files ..."

for ENV_VAR in $ENV_VARS_LIST; do
    echo "INFO:  Processing variable: $ENV_VAR"
    find . -name ".git" -prune -o -type f ! -name "init.sh" ! -name ".env-init" -exec sed -i '' "s|<$ENV_VAR>|${!ENV_VAR}|g" {} +
    #grep -rlE "\<$ENV_VAR\>" . | grep -vE "(\.git|init.sh|\.env-init)"
    #FILES_TO_REPLACE_LIST=$(grep -rlE "\<$ENV_VAR\>" . --exclude-dir=.git --exclude=init.sh --exclude=.env-init)
    echo $FILES_TO_RENAME_LIST
    # for FILE_TO_REPLACE in $FILES_TO_REPLACE_LIST; do
    #     echo "INFO:  Replacing \"<$ENV_VAR>\" with \"${!ENV_VAR}\" in $FILE_TO_REPLACE"
    #     if [ -z "$DRY_RUN" ]; then
    #     echo "INFO:  Replacing in $FILE_TO_REPLACE"
    # #        sed -i.bak "s|<$ENV_VAR>|${!ENV_VAR}|g" "$FILE_TO_REPLACE" && rm "$FILE_TO_REPLACE.bak"
    #     fi
    # done
done

# echo -e "\nINFO:  Cleaning up ..."
# echo "INFO:  Delete .env-init"
# if [ -z "$DRY_RUN" ]; then
#     rm .env-init
# fi

# echo "INFO:  Remove template init from justfile"
# if [ -z "$DRY_RUN" ]; then
#     sed -i '10,13d' justfile
# fi
