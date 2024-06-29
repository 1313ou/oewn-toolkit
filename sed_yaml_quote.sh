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

GREP='^  \- ###.*###$'
SED='s|^  \- ###\(.*\)###$|  - "\1"|'

GREP='^  \- ###.*$'
SED='s|^  \- ###|  - "|'

GREP='^.*###$'
SED='s|###$|"|'

echo -e "${Y}${GREP}${Z}"
echo -e "${Y}${SED}${Z}"
echo
for f in $(find -L "${DIR}" -name 'noun*' -o -name 'verb*' -o -name 'adj*' -o -name 'adv*' | sort); do
    #echo -e "${B}${f}${Z}"
    #grep -Hno -E "${GREP}" "${f}" | tr ':' '\t'
    data=$(grep -Hno -E "${GREP}" "${f}" | tr ':' '\t')
    IFS=$'\n'
    for datum in ${data}; do
        echo -e "${M}${datum}${Z}"

        lineno=$(echo "${datum}" | awk -F '\t' '{print $2}')
        change=$(echo "${datum}" | awk -F '\t' '{print $3}')
        #echo "${f} @ ${lineno}"
        if [ -z "${lineno}" ]; then
          echo -e "no lineno ${R}${datum}${Z}"
          continue
        fi

        change2=$(sed -n "${lineno}${SED}p" "${f}")
        if [ -z "${change2}" ]; then
          echo -e "unchanged ${R}${datum}${Z}"
          continue
        fi
        echo -e "${B}${change2}${Z}"

        #if confirm "${change}"; then
          if [ ! -z "${MODIFY}" ]; then
              sed -i "${lineno}${SED}" "${f}"
          fi
        #else
        #  if confirm "edit ${f}:${lineno}"; then
        #    wait_for_kate --line ${lineno} "${f}"
        #  fi
        #fi
    done
    #break
done

