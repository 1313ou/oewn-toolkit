#!/bin/bash

echo -e "${Z}"

source define_colors.sh

function ask_modify() {
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
}

export MODIFY=$(ask_modify $@)