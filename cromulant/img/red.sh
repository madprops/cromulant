#!/usr/bin/env bash

convert $1 -channel R -evaluate add 16% +channel -quality 85 -strip $1_red