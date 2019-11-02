#!/bin/bash

find imageapi -name "*jpg" | while read i
do
    echo $i
    mogrify -auto-orient "$i"
done
