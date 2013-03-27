#!/bin/bash

echo $1
rename 's/^$1/$2/' $1*

