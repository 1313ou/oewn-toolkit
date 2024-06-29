#!/bin/bash
# Tabular file provides provides OEWN synset ids to edit.
# Each row's first (tab-separated) column contains the OEWN synset to edit.

source define_colors.sh
source define_kate.sh
echo -e "${Z}"

FILE=.
if [ ! -z "$1" ]; then
  FILE="$1"
fi
echo -e "Processed file: ${M}$FILE${Z}"

DIR=.
if [ ! -z "$2" ]; then
  DIR="$2"
fi
echo -e "Target directory: ${Y}${DIR}${Z}"

while read -r line; do
  # extract first column
  oewnsynsetid=$(echo "${line}" | awk '{print $1}')
  if [ -z "${oewnsynsetid}" ]; then
    continue
  fi
  echo -e "${B}${oewnsynsetid}${Z}"
  # find where it's defined (file --H, line number -- n)
  r=$(grep -Hn "^${oewnsynsetid}" "${DIR}"/*)
  # split
  f=$(echo "${r}" | awk -F  ':' '{print $1}')
  l=$(echo "${r}" | awk -F  ':' '{print $2}')
  echo -e "${C}${f} @ ${l}${Z}"
  # run
  wait_for_kate --line "${l}" "${f}"
  
done < "${FILE}"
