#!/usr/bin/env bash

convert $1 -channel G -evaluate add 16% +channel -quality 85 -strip $1_green
