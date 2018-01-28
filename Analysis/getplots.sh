#!/bin/bash

#open plots
FILES=$(ls plots/)

for f in $FILES
do
	xdg-open plots/$f
done
