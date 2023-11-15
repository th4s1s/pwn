#!/bin/sh
while true
do
    rm -rf payload
    ln -s touch payload
    rm -rf payload
    ln -s payload.txt payload
done