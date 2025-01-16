#!/usr/bin/env bash
cd cromulant
clear &&
ruff format && ruff check &&
mypy --strict --strict --strict main.py &&
pyright