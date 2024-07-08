#!/bin/bash

source define_colors.sh
source define_kate.sh
echo -e "${Z}"

DIR="$1"
shift
if [ ! -d "${DIR}" ]; then
  exit 1
fi
echo -e "Target directory: ${Y}${DIR}${Z}"

if [ -z "$*" ]; then
  exit 1
fi

for REGEX in "$@"; do
   echo "${REGEX}"
   grep -Hn "${REGEX}" "${DIR}"/* | awk -F ':' '{print $2,$1}' | while read -r line; do
    echo -e "${C}${line}${Z}"
    wait_for_kate --line ${line}
  done
done