# -----------------------------------------------------------
# Script that performs a pokemon swap in a pokecrystal 
# disassembly project. This will not add a pokedex entry, 
# evolutions, moves and other more subtle changes but it will 
# reduce the number of files to modify
#
# (C) 2022 Gyros Team, Spain
# Released under GNU Public License (GPL)
# email arzdou@gmail.com
# -----------------------------------------------------------

import os, sys, logging

# Swap and comment function
def swap_and_comment(old: str, new: str, path: str, exit_if_error=True):
        """
        Swap all ocurrences of "old" to "new" in a file given by path 
        and comment out the change
        
        Parameters:

        - old: text to swap
        - new: text to replace with
        - path: location to the .asm file
        - exit_if_error (Optional): Whether to close the execution if 
                                    the program detects and error
        """
        if not os.path.isfile(path):
            logging.error("File doesn't exist: " + path)
            sys.exit()
        
        with open(path, "r") as f:
            text = f.read()
            
        if old not in text and exit_if_error:
            logging.error("Old pokemon doesn't exist in " + path)
            sys.exit()
            
        if new in text and exit_if_error:
            logging.error("New pokemon already in " + path)
            sys.exit()
            
        lines = text.split("\n")
        new_lines = []
        for l in lines:
            if old in l:
                new_lines.append(l.replace(old, new, 1)+" ; +")
                new_lines.append(";"+l)
            else:
                new_lines.append(l)
        new_text = "\n".join(new_lines)

        with open(path, "w") as f:
            f.write(new_text)
            
        return 0

if __name__ == "__main__":
    
    args = sys.argv
    if len(args) < 3:
        logging.error("Need two arguments to be able to perform the swap")
        sys.exit()
    if len(args) > 3:
        logging.warning("More than 2 arguments were given, only first two will be used")

    old_pokemon = args[1].lower()
    new_pokemon = args[2].lower()

    # Constants
    swap_and_comment(
        old=old_pokemon.upper(),
        new=new_pokemon.upper(),
        path="./constants/pokemon_constants.asm"
    )

    # Names
    swap_and_comment(
        old=old_pokemon.upper().ljust(10, "@"),
        new=new_pokemon.upper().ljust(10, "@"),
        path="./data/pokemon/names.asm"
    )

    # Base stats import
    swap_and_comment(
        old=old_pokemon,
        new=new_pokemon,
        path="./data/pokemon/base_stats.asm"
    )

    # Evolutions and attacks pointers
    swap_and_comment(
        old=old_pokemon.capitalize(),
        new=new_pokemon.capitalize(),
        path="./data/pokemon/evos_attacks_pointers.asm"
    )

    # Egg moves pointers
    swap_and_comment(
        old=old_pokemon.capitalize(),
        new=new_pokemon.capitalize(),
        path="./data/pokemon/egg_move_pointers.asm",
        exit_if_error=False  # Some pokemon don't have egg moves assigned to them.
    )

    # Cries, sets the same cry as the swapped pokemon
    swap_and_comment(
        old="; "+old_pokemon.upper(),
        new="; "+new_pokemon.upper(),
        path="./data/pokemon/cries.asm",
    )


    # Menu Icons, sets the same icon as the swapped pokemon
    swap_and_comment(
        old="; "+old_pokemon.upper(),
        new="; "+new_pokemon.upper(),
        path="./data/pokemon/menu_icons.asm",
    )


    # Dex entry pointers
    swap_and_comment(
        old=old_pokemon.capitalize(),
        new=new_pokemon.capitalize(),
        path="./data/pokemon/dex_entry_pointers.asm",
    )

    # Dex order new pointers
    swap_and_comment(
        old=old_pokemon.upper(),
        new=new_pokemon.upper(),
        path="./data/pokemon/dex_order_new.asm",
    )

    # Footprint import
    swap_and_comment(
        old=old_pokemon,
        new=new_pokemon,
        path="./gfx/footprints.asm",
    )

    # Pic pointers
    swap_and_comment(
        old=old_pokemon.capitalize(),
        new=new_pokemon.capitalize(),
        path="./data/pokemon/pic_pointers.asm",
    )

    # Pics
    swap_and_comment(
        old=old_pokemon,
        new=new_pokemon,
        path="./gfx/pics.asm",
    )
    swap_and_comment(
        old=old_pokemon.capitalize(),
        new=new_pokemon.capitalize(),
        path="./gfx/pics.asm",
    )

    # Palettes
    swap_and_comment(
        old=old_pokemon,
        new=new_pokemon,
        path="./data/pokemon/palettes.asm",
    )

    # Animation pointers
    swap_and_comment(
        old=old_pokemon.capitalize(),
        new=new_pokemon.capitalize(),
        path="./gfx/pokemon/anim_pointers.asm",
    )

    # Animation imports
    swap_and_comment(
        old=old_pokemon,
        new=new_pokemon,
        path="./gfx/pokemon/anims.asm",
    )
    swap_and_comment(
        old=old_pokemon.capitalize(),
        new=new_pokemon.capitalize(),
        path="./gfx/pokemon/anims.asm",
    )

    # Idle pointers
    swap_and_comment(
        old=old_pokemon.capitalize(),
        new=new_pokemon.capitalize(),
        path="./gfx/pokemon/idle_pointers.asm",
    )

    # Idle imports
    swap_and_comment(
        old=old_pokemon,
        new=new_pokemon,
        path="./gfx/pokemon/idles.asm",
    )
    swap_and_comment(
        old=old_pokemon.capitalize(),
        new=new_pokemon.capitalize(),
        path="./gfx/pokemon/idles.asm",
    )

    # Bitmask pointers
    swap_and_comment(
        old=old_pokemon.capitalize(),
        new=new_pokemon.capitalize(),
        path="./gfx/pokemon/bitmask_pointers.asm",
    )

    # Bitmask imports
    swap_and_comment(
        old=old_pokemon,
        new=new_pokemon,
        path="./gfx/pokemon/bitmasks.asm",
    )
    swap_and_comment(
        old=old_pokemon.capitalize(),
        new=new_pokemon.capitalize(),
        path="./gfx/pokemon/bitmasks.asm",
    )

    # Frame pointers
    swap_and_comment(
        old=old_pokemon.capitalize(),
        new=new_pokemon.capitalize(),
        path="./gfx/pokemon/frame_pointers.asm",
    )

    # Kanto frames
    swap_and_comment(
        old=old_pokemon,
        new=new_pokemon,
        path="./gfx/pokemon/kanto_frames.asm",
        exit_if_error=False
    )
    swap_and_comment(
        old=old_pokemon.capitalize(),
        new=new_pokemon.capitalize(),
        path="./gfx/pokemon/kanto_frames.asm",
        exit_if_error=False
    )

    # Kanto frames
    swap_and_comment(
        old=old_pokemon,
        new=new_pokemon,
        path="./gfx/pokemon/johto_frames.asm",
        exit_if_error=False
    )
    swap_and_comment(
        old=old_pokemon.capitalize(),
        new=new_pokemon.capitalize(),
        path="./gfx/pokemon/johto_frames.asm",
        exit_if_error=False
    )

    # Gen 1 order
    swap_and_comment(
        old=old_pokemon.upper(),
        new=new_pokemon.upper(),
        path="./data/pokemon/gen1_order.asm",
        exit_if_error=False
    )

    # ezchat order
    swap_and_comment(
        old=old_pokemon.upper(),
        new=new_pokemon.upper(),
        path="./data/pokemon/ezchat_order.asm",
        exit_if_error=False
    )

    # Trainer parties
    swap_and_comment(
        old=old_pokemon.upper(),
        new=new_pokemon.upper(),
        path="./data/trainers/parties.asm",
        exit_if_error=False
    )
