#!/bin/bash
# This script transforms GSC pokemon sprites to be usable on the GBC

# USAGE: make-sprite.sh path/to/folder pokemon-number frames-in-sprite-sheet
# 1 - path e.g. 'gfx/pokemon/pikachu'
# 2 - number used to find images to convert e.g. '400' for 400.png and 400b.png
# 3 - frames in spritesheet e.g. 4

# FRONT
convert $1/$2.png -sample 50% -background white -alpha remove -alpha off $1/front.png
mogrify $1/front.png -type palette -fill "#FFFFFF" -opaque "#F8F8F8" -fuzz 10% $1/front.png
# convert $1/front.png  -depth 2 -type palette $1/front.png
convert $1/front.png -colors 4 -type palette $1/front.png

fw=$(identify -format '%w' "$1/front.png")
fh=$(identify -format '%h' "$1/front.png")

if [[ (($fw == 64)) || (($fh == 64)) ]] ; then
	echo "Image $1/front.png is 64x64, will be trimmed to 56x56"
	convert $1/front.png -gravity center -crop 56x56+0+0 +repage $1/front.png
fi

# turn to spritesheet
montage $1/front.png -duplicate $(($3-1)) -tile 1x$3 -geometry +0+0 $1/front.png
convert $1/front.png -depth 8 $1/front.png


# BACK
convert $1/$2b.png -sample 50% -background white -alpha remove -alpha off $1/back.png
mogrify $1/back.png -fill "#FFFFFF" -opaque "#F8F8F8" -fuzz 10% $1/back.png
convert $1/back.png -depth 8 -colors 4 -type palette $1/back.png

fw=$(identify -format '%w' "$1/back.png")
fh=$(identify -format '%h' "$1/back.png")

if [[ (($fw == 64)) || (($fh == 64)) ]] ; then
	echo "Image $1/back.png is 64x64, will be trimmed to 56x56"
	convert $1/back.png -gravity center -crop 56x56+0+0 +repage $1/back.png
fi


