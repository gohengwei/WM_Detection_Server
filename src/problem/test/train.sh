#!/bin/bash

svm-scale -l 0 -u 1 -s range $1 > $1.scale
svm-scale -l 0 -u 1 -r range $2 > $2.scale
svm-train -s 0 -t 2 -c $3 -g $4 $1.scale
svm-train -s 0 -t 2 -c $3 -g $4 -v 5 $1.scale
svm-predict $2.scale $1.scale.model $1.output



