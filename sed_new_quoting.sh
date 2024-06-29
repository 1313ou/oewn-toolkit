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

# ' 27 apostrophe
# ‟double quoted”
# “ 201C double quotation mark, left
# ” 201D double quotation mark, right

SEDa="s/###/＇/g"
SEDq1="s/<<</“/g"
SEDq2="s/>>>/”/g"
SED="${SEDa} ; ${SEDq1} ; ${SEDq2}"
SEDp="${SEDa}p ; ${SEDq1}p ; ${SEDq2}p"

#SED="${SEDq1} ; ${SEDq2}"
#SEDp="${SEDq1}p ; ${SEDq2}p"

for f in $(find -L "${DIR}" -name 'noun*' -o -name 'verb*' -o -name 'adj*' -o -name 'adv*' | sort); do
    echo -e "${Y}${f}${Z}"
 
    echo -e "${B}"
    sed -n "${SEDp}" "${f}"
    echo -e "${Z}"

    if [ ! -z "${MODIFY}" ]; then
      sed -i "${SED}" "${f}"
    fi
done
