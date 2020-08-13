#!/usr/bin/env python3

#external modules
from PIL import Image
import sys
#from pyfiglet import Figlet
from pathlib import Path

#internal modules
from game_map import Game_Map
import menu

def main(title=True):
    """Converts an image into an import-ready shmeppy map."""

    #get user inputs from menu
    try:
        img_path = sys.argv[1]
    except:
        print("Image file not provided.")
        img_path=None
    answers = menu.main_menu(img_path)

    #process user inputs
    if answers['debug']: print(answers)
    try:
        map_size = (answers['map_dim_x'],answers['map_dim_y'])
    except:
        map_size = (answers['map_major_dim'])
    gm = Game_Map(answers['img_path'],map_size,answers['debug'])

    if answers['op_type'].startswith('pal'):
        op = gm.palette_op(answers['palette_size'], sample_factor = answers['sample_factor'])
    elif answers['op_type'].startswith('fil'):
        op = gm.filter_op(answers['filter_type'])
    else:
        print("Sorry, something went wrong.")

    result = gm.op_to_json(op)
    print(result)


if __name__ == '__main__':
    main()
