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

# “ 201C double quotation mark, left
# ” 201D double quotation mark, right
# “quoted”

A="´"
Q1="“"
Q2="”"
SEDq1="s/\`/${Q1}/g"
SEDq2="s/$A/${Q2}/g"
SEDbacktick="s/${Q1}${Q1}${Q2}/${Q1}\`${Q2}/g"

SED="${SEDq1} ; ${SEDq2} ; ${SEDbacktick}"
echo $SED
SEDp="${SEDq1}p ; ${SEDq2}p ; ${SEDbacktick}p"
echo $SEDp

function change() {
    sed -n "${SEDp}" $@
}

function change_in_file() {
     sed -i "${SED}" $@
}

function main() {
  for f in $(find -L "${DIR}" -name 'noun*' -o -name 'verb*' -o -name 'adj*' -o -name 'adv*' | sort); do
     echo -e "${Y}${f}${Z}"
 
     echo -en "${B}"
     change "${f}"
     echo -en "${Z}"

     if [ ! -z "${MODIFY}" ]; then
       change_in_file "${f}"
     fi
  done
}

main