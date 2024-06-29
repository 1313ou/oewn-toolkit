#!/bin/bash

#
# Copyright (c) 2024. Bernard Bou.
#

function confirm() {
    echo -en "${G}${1}${Z}"
    read -p " ?> " -n 1 -r
    echo -e "${Z}"
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        return 0
    fi
    return 1
}

