#!/bin/bash

source define_colors.sh
echo -e "${Z}"

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

GREP='…\S'
SED='s/…\(\S\)/… \1/g'

for f in $(find -L "${DIR}" -name 'noun*' -o -name 'verb*' -o -name 'adj*' -o -name 'adv*' | sort); do
    if grep -Hn "${GREP}" "${f}";then
        echo -e "${Y}${f}${Z}"
        
        echo -e "${B}"
        sed -n "${SED}p" "${f}"
        echo -e "${Z}"
        
        if [ ! -z "${MODIFY}" ]; then
            sed -i "${SED}" "${f}"
        fi
    fi
done

