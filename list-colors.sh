#!/bin/bash
# This script lists the colors in an in put image

# USAGE: list-colors.sh path/to/image

convert $1 -define histogram:unique-colors=true -format %c histogram:info:-
