#!/bin/bash
chal="${CHAL:-bksec-pwn-babyservice}"
docker rm -f "$chal"
docker build --tag="$chal" .
docker run -d -p 1337:1337 --name="${chal}" "${chal}"