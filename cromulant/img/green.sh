#!/usr/bin/env bash

convert $1 -channel G -evaluate add 12% +channel -quality 85 -strip $1_green