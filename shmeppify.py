#!/usr/bin/env python3

#external modules
from PIL import Image
import sys
#from pyfiglet import Figlet
from pathlib import Path

#internal modules
from game_map import Game_Map
import menu

def run(title=True):
    """Converts an image into an import-ready shmeppy map."""

    #get user inputs from menu
    answers = {}
    try:
        img_path = sys.argv[1]
        answers['img_path'] = img_path
    except:
        img_path = False
    answers.update(menu.main(img_path))

    #exit if exit
    if answers['op_type'].startswith('exit'):
        sys.exit()
    elif answers['op_type'].startswith('help'):
        p = Path("help.txt")
        with open(p, encoding="utf8") as ht:
            print(ht.read())
        return run(title=False)

    #process user inputs
    if answers['debug']: print(answers)
    map_size = (answers['map_dim_x'],answers['map_dim_y'])
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
    run()
