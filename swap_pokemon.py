# -----------------------------------------------------------
# Script that performs a pokemon swap in a pokecrystal 
# disassembly project. The pokemon information necessary to 
# create the base stats file and update the evoattacks and 
# eggmoves file is obtained from pokeAPI and parsed into their 
# corresponding formats. The script will only include moves 
# that are defined within the project and discard the rest.
#
# Sprite, animations and footprint must be done manualy.
#
# (C) 2022 Gyros Team, Spain
# Released under GNU Public License (GPL)
# email arzdou@gmail.com
# -----------------------------------------------------------

import os, sys, logging, requests
from shutil import rmtree
from json.decoder import JSONDecodeError


# Swap and comment function
def swap_and_comment(old: str, new: str, path: str, comment=True, exit_if_error=True):
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
                if comment:
                    new_lines.append(";"+l)
            else:
                new_lines.append(l)
        new_text = "\n".join(new_lines)

        with open(path, "w") as f:
            f.write(new_text)
            
        return 0
    
def call_pokeapi(pokemon_name):
    response = requests.get('https://pokeapi.co/api/v2/pokemon/'+pokemon_name)
    pokemon_data = response.json()
    response = requests.get(pokemon_data['species']['url'])
    species_data = response.json()

    # Level up, Egg and TM Moves

    # Read the moves defined for this pokecrystal project
    with open("./constants/move_constants.asm", "r") as f:
        move_text_asm = f.read()
    move_list = []
    for m in move_text_asm.split('\n')[:260]:
        if 'const ' in m:
            move_name = ''.join(filter(lambda c: c.isupper() or c=='_', m))
            move_list.append(move_name)
    
    # Read the tm items defined for this pokecrystal project
    with open("./constants/item_constants.asm", "r") as f:
        item_text_asm = f.read()
    start_tm = 218 # Where the TM items starts and end
    end_tm = 272
    tm_list = []
    for m in item_text_asm.split('\n')[start_tm:end_tm]:
        if 'add_tm ' in m:
            move_name = ''.join(filter(lambda c: c.isupper() or c=='_', m))
            tm_list.append(move_name[1:]) # The filtering carries an extra _
            
    level_moves = {}
    egg_moves = []
    tm_moves = []
    for move_json in pokemon_data['moves']:
        name = move_json['move']['name'].upper().replace('-', '_', 10)
        method = move_json['version_group_details'][0]['move_learn_method']['name']
        level = move_json['version_group_details'][0]['level_learned_at']
        
        if name not in move_list:
            continue
        
        if method in ['machine', 'tutor'] and name in tm_list:
            tm_moves.append(name)
        elif method == 'egg':
            egg_moves.append(name)
        elif level > 0:
            level_moves[name] = level
    level_moves = dict(sorted(level_moves.items(), key=lambda item: item[1]))
    
    # Types
    pokemon_types = [types_json['type']['name'].upper() for types_json in pokemon_data['types']]
    if len(pokemon_types) == 1:
        pokemon_types.append(pokemon_types[0])
    
    # Items
    held_items = [item['item']['name'].upper().replace('-', '_', 10) for item in pokemon_data['held_items']]
    for _ in range( max(2-len(held_items), 0) ):
        held_items.append('NO_ITEM')
        
    # Growth rate
    growth_rate_dict = {
        'medium': 'GROWTH_MEDIUM_FAST',
        'fast then very slow': 'GROWTH_SLIGHTLY_SLOW',
        'slow then very fast': 'GROWTH_SLIGHTLY_FAST',
        'medium-slow': 'GROWTH_MEDIUM_SLOW',
        'fast': 'GROWTH_FAST',
        'slow': 'GROWTH_SLOW'
    }
    
    # Gender rate
    gender_ratio_dict = {
        0: 'GENDER_F0',
        1: 'GENDER_F12_5',
        2: 'GENDER_F25',
        4: 'GENDER_F50',
        6: 'GENDER_F75',
        8: 'GENDER_F100',
        -1: 'GENDER_UNKNOWN',
    }
    
    # Egg group
    egg_group_dict = {
        'monster': 'EGG_MONSTER',  
        'water1': 'EGG_WATER_1',   
        'bug': 'EGG_BUG',    
        'flying': 'EGG_FLYING',   
        'ground': 'EGG_GROUND',   
        'fairy': 'EGG_FAIRY',     
        'plant': 'EGG_PLANT',   
        'human-shape': 'EGG_HUMANSHAPE',  
        'water3': 'EGG_WATER_3',   
        'mineral': 'EGG_MINERAL',      
        'indeterminate': 'EGG_INDETERMINATE',
        'water2': 'EGG_WATER_2',       
        'ditto': 'EGG_DITTO',        
        'dragon': 'EGG_DRAGON',      
        'no-eggs': 'EGG_NONE',
    }
    
    egg_group = [egg_group_dict[egg_json['name']] for egg_json in species_data['egg_groups']]
    if len(egg_group) == 1:
        egg_group.append(egg_group[0])
        
    # Species
    for s in species_data['genera']:
        if s['language']['name'] == 'en':
            species = s["genus"][:-8].upper()
            
    # Dex entry
    dex_entry = species_data['flavor_text_entries'][0]['flavor_text']
    dex_entry = dex_entry.replace('\u000c', '\n', 10).replace('POKé', '#', 10).replace('’', '', 10)
    dex_entry += '@'
    dex_entry = dex_entry.splitlines(),
    
    # Return argument
    out = {
        'name': pokemon_name,
        'species': species,
        'stats': {stat_json['stat']['name']: stat_json['base_stat'] for stat_json in pokemon_data['stats']},
        'types': pokemon_types,
        'items': held_items,
        'catch_rate': species_data['capture_rate'],
        'base_exp': pokemon_data['base_experience'],
        'gender_ratio': gender_ratio_dict[species_data['gender_rate']],
        'step_cycles': species_data['hatch_counter'],
        'growth_rate': growth_rate_dict[species_data['growth_rate']['name']],
        'egg_groups': egg_group,
        'height': pokemon_data['height'],
        'weight': pokemon_data['weight'],
        'dex_entry': dex_entry,
        'moves': {
            'level': level_moves,
            'egg': egg_moves,
            'tm': tm_moves
        }
    }

    return out

if __name__ == "__main__":
      
    args = sys.argv
    if len(args) < 3:
        logging.error("Need two arguments to be able to perform the swap")
        sys.exit()
    if len(args) > 3:
        logging.warning("More than 2 arguments were given, only first two will be used")
    
    old_pokemon = args[1].lower()
    new_pokemon = args[2].lower()
    
    # Add exception handling for custom pokemon
    try:
        new_pokemon_data = call_pokeapi(new_pokemon)
    except JSONDecodeError:
        logging.error("The pokemon to add was not found in the database")
        sys.exit()

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
    
    # Rename gfx pokemon and footprint directories to allow assembly
    try: 
        os.rename('./gfx/pokemon/'+old_pokemon, './gfx/pokemon/'+new_pokemon)
    except FileExistsError:
        delete_dir = input('An existent directory was found at %s, do you want to delete it? (Y/n): '%('./gfx/pokemon/'+new_pokemon))
        while True:
            if delete_dir.lower() in ['y', 'yes']:
                print('Directory deleted')
                rmtree('./gfx/pokemon/'+new_pokemon)
                os.rename('./gfx/pokemon/'+old_pokemon, './gfx/pokemon/'+new_pokemon)
                break
            elif delete_dir.lower() in ['n', 'no']:
                print('Directory was not deleted')
                break
            else: 
                delete_dir = input('Not a valid answer, please retry (Y/n): ')

        
            
    os.rename('./gfx/footprints/'+old_pokemon+'.png', './gfx/footprints/'+new_pokemon+'.png')
    
    # Base stats
    # Construct a new file for the new pokemon
    base_stats_text = []
    base_stats_text.append('\tdb '+new_pokemon_data['name'].upper())
    base_stats_text.append('')
    base_stats_text.append(
        '\tdb ' + 
        str(new_pokemon_data['stats']['hp']) + ', ' + 
        str(new_pokemon_data['stats']['attack']) + ', ' +
        str(new_pokemon_data['stats']['defense']) + ', ' +
        str(new_pokemon_data['stats']['special-defense']) + ', ' +
        str(new_pokemon_data['stats']['special-attack']) + ', ' +
        str(new_pokemon_data['stats']['speed']) + ', ' 
    )
    base_stats_text.append('\t;   hp  atk  def  spd  sat  sdf')
    base_stats_text.append('')
    base_stats_text.append('\tdb ' + ', '.join(new_pokemon_data['types']) + ' ; type')
    base_stats_text.append('\tdb ' + str(new_pokemon_data['catch_rate']) + ' ; catch rate')
    base_stats_text.append('\tdb ' + str(new_pokemon_data['base_exp']) + ' ; base exp')
    base_stats_text.append('\tdb ' + ', '.join(new_pokemon_data['items']) + ' ; items')
    base_stats_text.append('\tdb ' + str(new_pokemon_data['gender_ratio']) + ' ; gender ratio')
    base_stats_text.append('\tdb 100 ; unkown 1')
    base_stats_text.append('\tdb ' + str(new_pokemon_data['step_cycles']) + ' ; step cycles to hatch')
    base_stats_text.append('\tdb 5 ; unkown 2')
    base_stats_text.append('\tINCBIN "gfx/pokemon/' + new_pokemon_data['name'] + '/front.dimensions"')
    base_stats_text.append('\tdw NULL, NULL ; unused (beta front/back pics)')
    base_stats_text.append('\tdb ' + new_pokemon_data['growth_rate'] + ' ; growth rate')
    base_stats_text.append('\tdn ' + ', '.join(new_pokemon_data['egg_groups']) + ' ; egg groups')
    base_stats_text.append('')
    base_stats_text.append('\t; tm/hm learnset')
    base_stats_text.append('\ttmhm ' + ', '.join(new_pokemon_data['moves']['tm']))
    base_stats_text.append('\t; end')
    base_stats_text.append('')

    with open('./data/pokemon/base_stats/%s.asm'%new_pokemon, 'w') as f:
        f.write('\n'.join(base_stats_text))

    # Base stats import
    swap_and_comment(
        old=old_pokemon,
        new=new_pokemon,
        path="./data/pokemon/base_stats.asm"
    )
    
    # Evolutions and attacks
    #
    # Construct a new block of evos_attacks for the new pokemon
    new_evos_attacks = []
    new_evos_attacks.append(new_pokemon_data['name'].capitalize() + 'EvosAttacks: ; +')
    new_evos_attacks.append('\tdb 0 ; ADD YOUR EVOLUTION') 
    for move, level in new_pokemon_data['moves']['level'].items():
        new_evos_attacks.append('\tdb %d, %s'%(level, move))
    new_evos_attacks.append('\tdb 0 ; no more level-up moves') 
    
    # Write this new block and comment out the old pokemon in the correct file
    with open('./data/pokemon/evos_attacks.asm', 'r') as f:
        evos_attacks_text = f.read()

    evos_attacks_blocks = evos_attacks_text.split('\n\n')
    block_index = [i for i, b in enumerate(evos_attacks_blocks) if old_pokemon.capitalize()+'EvosAttacks' in b][0]

    commented_block = []
    for l in evos_attacks_blocks[block_index].split('\n'):
        commented_block.append(';'+l)
        
    evos_attacks_blocks[block_index] = '\n'.join(commented_block)
    evos_attacks_blocks.insert(block_index, '\n'.join(new_evos_attacks))

    with open('./data/pokemon/evos_attacks.asm', 'w') as f:
        f.write('\n\n'.join(evos_attacks_blocks))
    
    
    # Evolutions and attacks pointers
    swap_and_comment(
        old=old_pokemon.capitalize(),
        new=new_pokemon.capitalize(),
        path="./data/pokemon/evos_attacks_pointers.asm"
    )
    
    # Egg moves
    #
    # Some pokemon dont have egg moves and thus we have to avoid 
    # writting unnecesary data
    with open('./data/pokemon/egg_moves.asm', 'r') as f:
        egg_moves_text = f.read()
    egg_moves_blocks = egg_moves_text.split('\n\n')

    # Check if there is a block of eggmoves for the old pokemon and comment it out
    if old_pokemon.capitalize()+'EggMoves' in egg_moves_text:
        block_index = [i for i, b in enumerate(egg_moves_blocks) if old_pokemon.capitalize()+'EggMoves' in b][0]

        commented_block = []
        for l in egg_moves_blocks[block_index].split('\n'):
            commented_block.append(';' + l)
            
        egg_moves_blocks[block_index] = '\n'.join(commented_block)
        
    else:
        # If no egg moves are found the inserting index is before NoEggMoves
        block_index = -1

    # If the new pokemon has egg moves, add a block in the asm file
    if new_pokemon_data['moves']['egg']:
        new_egg_moves = []
        new_egg_moves.append(new_pokemon_data['name'].capitalize() + 'EggMoves:')
        for m in new_pokemon_data['moves']['egg']:
            new_egg_moves.append('\tdb ' + m)
        new_egg_moves.append('\tdb -1 ; end')
        egg_moves_blocks.insert(block_index, '\n'.join(new_egg_moves))
    
    with open('./data/pokemon/egg_moves.asm', 'w') as f:
        f.write('\n\n'.join(egg_moves_blocks))

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

    # Dex entry file
    #
    # Construct the file and addit to the dex entries. It is most 
    # likely that the spacing on the extry is incorrect since it
    # will be adapted for future generations
    dex_entry_text = []
    dex_entry_text.append('\tdb "%s@" ; species name'%new_pokemon_data['species'])
    dex_entry_text.append('\tdb %d, %d ; height, weight'%(new_pokemon_data['height'], new_pokemon_data['weight']))
    dex_entry_text.append('\n')

    for i, line in enumerate(new_pokemon_data['dex_entry'][0]):
        if i == 0:
            dex_entry_text.append('\tdb   "%s"'%line)
        elif i%3 == 0:
            dex_entry_text.append('\n')
            dex_entry_text.append('\tpage "%s"'%line)
        else:
            dex_entry_text.append('\tnext "%s"'%line)
    dex_entry_text.append('\n')

    with open('./data/pokemon/dex_entries/%s.asm'%new_pokemon, 'w') as f:
        f.write('\n'.join(dex_entry_text))
        
    swap_and_comment(
        old=old_pokemon,
        new=new_pokemon,
        path="./data/pokemon/dex_entries.asm",
        comment=False
    )
    swap_and_comment(
        old=old_pokemon.capitalize(),
        new=new_pokemon.capitalize(),
        path="./data/pokemon/dex_entries.asm"
    )

    # Dex entry pointers
    swap_and_comment(
        old=old_pokemon.capitalize(),
        new=new_pokemon.capitalize(),
        path="./data/pokemon/dex_entry_pointers.asm",
    )
    
    # Dex order alpha
    #
    # Read the pokemon in alphanumeric order, search the pokemon to comment out 
    # and then insert the new pokemon in the correct position
    with open('./data/pokemon/dex_order_alpha.asm', 'r') as f:
        dex_alpha_text = f.read()
    dex_alpha_lines = dex_alpha_text.split('\n')

    dex_alpha_pokemon = [new_pokemon.upper()]
    for i, m in enumerate(dex_alpha_lines):
        if '\tdb ' in m and ';' not in m:
            dex_alpha_name = ''.join(filter(lambda c: c.isupper() or c=='_', m))
            dex_alpha_pokemon.append(dex_alpha_name)
            if dex_alpha_name == old_pokemon.upper():
                comment_index = i
                
    dex_alpha_pokemon.sort()
    dex_alpha_index = dex_alpha_pokemon.index(new_pokemon.upper())
    dex_alpha_lines[comment_index] = ';' + dex_alpha_lines[comment_index]
    dex_alpha_lines.insert(dex_alpha_index+4, '\tdb '+new_pokemon.upper())

    with open('./data/pokemon/dex_order_alpha.asm', 'w') as f:
        f.write('\n'.join(dex_alpha_lines))
        
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
        comment=False
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
        comment=False
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
        comment=False
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
        comment=False
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
        comment=False,
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
        comment=False,
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
