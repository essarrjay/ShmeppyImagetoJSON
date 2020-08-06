#!/usr/bin/env python3

#external modules
from PIL import Image
import sys
from pyfiglet import Figlet

#internal modules
from game_map import Game_Map
import menu



def run():
    #title
    f = Figlet(font='slant')
    print(f.renderText('Shemppy Image\nto JSON'))

    #get user inputs from menu
    answers = {}
    try:
        img_path = sys.argv[1]
        answers['img_path'] = img_path
    except:
        img_path = False
    answers.update(menu.main(img_path))

    #process user inputs
    #process_action = answers.pop('process_action')
    if answers['debug']: print(answers)
    gm = Game_Map(answers['img_path'],answers['max_map_dim'])

    if answers['process_action'].startswith('pal'):
        op = gm.palette_op(answers['palette_size'],answers['debug'])
    elif answers['process_action'].startswith('box'):
        op = gm.filter_op(Image.BOX,answers['debug'])
    else:
        print("Sorry, something went wrong.")

    result = gm.op_to_json(op)
    print(result)

if __name__ == '__main__':
    run()
