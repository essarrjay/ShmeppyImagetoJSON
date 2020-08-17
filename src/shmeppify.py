#!/usr/bin/env python3

#external modules
from PIL import Image
import sys
from pathlib import Path
import json

#internal modules
from game_map import Game_Map
import menu

#init globals
BASE_DIR = Path(__file__).parent
config_path = BASE_DIR.joinpath('config.json')
with open(config_path) as f:
    config_dict = json.load(f)
rescaling_factor = config_dict["rescaling_factor"]

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
    if answers['debug']: print(f' ► Answers: {answers}')
    try:
        map_size = (answers['map_dim_x'],answers['map_dim_y'])
        map_major_dim = max(map_size)
    except:
        map_major_dim = answers['map_major_dim']
        map_size = (answers['map_major_dim'])

    if answers['op_type'].startswith('pal'):
        #process palette operation
        if answers['palette_rescale']:
            #resize image before processing
            in_path = Path(answers['img_path'])
            temp_path = Path('resized_'+in_path.name)
            with Image.open(in_path) as im:
                size = min(rescaling_factor*map_major_dim,*im.size)
                im.thumbnail((size,size),resample=Image.LANCZOS)
                im.save(temp_path)
            answers['img_path'] = str(temp_path)

        #create Game_Map and Fill_Operation
        gm = Game_Map(answers['img_path'],map_size,answers['debug'])
        op = gm.palette_op(answers['palette_size'], sample_factor = answers['sample_factor'])

        #remove palette_rescale file if present
        if answers['palette_rescale']: temp_path.unlink(missing_ok=True)

    elif answers['op_type'].startswith('fil'):
        gm = Game_Map(answers['img_path'],map_size,answers['debug'])
        op = gm.filter_op(answers['filter_type'])
    else:
        print("Sorry, something went wrong.")

    #Export to Shmeppy map as a JSON file
    result = gm.op_to_json(op)
    print(result)

    #pause before exiting - necessary for pyinstaller
    input("Press Enter to Exit...")

if __name__ == '__main__':
    main()