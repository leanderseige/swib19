#!/bin/bash

find imageapi -name "*jpg" | while read i
do
    echo "converting $i"
    echo $(basename $i)
    convert "$i" -define tiff:tile-geometry=256x256 -compress jpeg -quality 96 "ptif:$i.tif"
done
