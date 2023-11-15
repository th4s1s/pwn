#!/bin/bash

mkdir $(cat flag.txt)
cd $(cat flag.txt)
mv ../chall .
./chall