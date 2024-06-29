#!/bin/bash
# OEWN synsetids are passed on the command-line

source define_colors.sh
source define_kate.sh
echo -e "${Z}"

DIR=.
if [[ ! $1 =~ [0-9]{8}-[nvars] ]]; then
  DIR="$1"
  shift
fi
echo -e "Target directory: ${Y}${DIR}${Z}"

# read command-line arguments
for oewnsynsetid in "$@"; do
  echo "${oewnsynsetid}"
  echo -e "${B}${oewnsynsetid}${Z}"
  # find where it's defined (file --H, line number -- n)
  r=$(grep -Hn "^${oewnsynsetid}" "${DIR}"/*)
  # split
  f=$(echo "${r}" | awk -F  ':' '{print $1}')
  l=$(echo "${r}" | awk -F  ':' '{print $2}')
  echo -e "${C}${f} @ ${l}${Z}"
  # run
  wait_for_kate --line ${l} "${f}"
  
done

