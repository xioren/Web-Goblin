#!/bin/bash

# *nix only
# run this after placing the program in the desired location
# pass u to uninstall


if [ $1 ] && [ $1 == 'u' ]
then
    rm $HOME/.local/bin/image-goblin && echo symlink removed
else
    ln -s $PWD/image_goblin/image_goblin.py $HOME/.local/bin/image-goblin && echo symlink created at $HOME/.local/bin/image-goblin
fi
