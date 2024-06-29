#!/bin/bash

echo -e "${Z}"

source define_colors.sh
source define_confirm.sh
source define_kate.sh

MODIFY=
if [ "-m" == "$1" ]; then
  MODIFY=true
  shift
  echo -e "${R}"
  read -p "Are you sure you want to modify data? " -n 1 -r
  echo    # (optional) move to a new line
  echo -e "${Z}"
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo 'Proceeding ...'
  else
    echo 'Cancelled ...'
    exit 2
  fi
fi

DIR=.
if [ ! -z "$1" ]; then
  DIR="$1"
fi
DIR=yaml

SED="s/###/'/g"

echo -e "${Y}${SED}${Z}"
echo

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

while read -u 3 -r line; do

  # extract first column
  oewnsynsetid=$(echo "${line}" | awk -F '\t' '{print $2}')
  target=$(echo "${line}" | awk -F '\t' '{print $1}')
  target2="^  - ${target}$"
  target2=${target2/-/\\-} # escaped
  if [ -z "${oewnsynsetid}" ]; then
    continue
  fi
  echo -e "${B}${oewnsynsetid} <${target}> <${target2}> ${Z}"

  # find where it's defined (file --H, line number -- n)
  r=$(grep -Hn "^${oewnsynsetid}" "${DIR}"/*)
  # split
  f=$(echo "${r}" | awk -F ':' '{print $1}')
  idlineno=$(echo "${r}" | awk -F ':' '{print $2}')
  beforelineno=$((idlineno+20))
  echo -e "${C}${f} @ ${idlineno}${Z}"

  # find target in synset scope
  r2=$(sed -n "${idlineno},${beforelineno}p" "${f}" | grep -n0 "${target2}" | tr ':' '\t')
  if [ -z "${r2}" ]; then
    echo -e "${R}${target}${Z} not found"
    continue
  fi
  scopelineno=$(echo "${r2}" | awk -F '\t' '{print $1}')
  t=$(echo "${r2}" | awk -F '\t' '{print $2}')
  lineno=$((idlineno + scopelineno - 1))
  echo -e "${Y}${f} @ ${idlineno}+${scopelineno}=${lineno} <${t}>${Z}"

  # assess change
  change=$(sed -n "${lineno}${SED}p" "${f}")
  echo -e "${LIGHT_MAGENTA}${t}${Z}"
  echo -e "${M}${change}${Z}"

  # enforce change
  if confirm "${change}"; then
    if [ ! -z "${MODIFY}" ]; then
      sed -i "${lineno}${SED}" "${f}"
    fi
  else
    if confirm "edit ${f}:${lineno}"; then
       wait_for_kate --line ${lineno} "${f}"
    fi
  fi

done 3< "${FILE}"
