#!/bin/bash

function wait_for_kate_back() {
  kate "$@" > /dev/null 2> /dev/null &
  pid=$! # or $(jobs -p)
  wait ${pid}
}

function wait_for_kate_poll() {
  kate "$@" > /dev/null 2> /dev/null
  while pgrep -x "kate" > /dev/null; do
    sleep 1
  done
}

function wait_for_kate() {
  kate --block "$@" > /dev/null 2> /dev/null
  wait
}
