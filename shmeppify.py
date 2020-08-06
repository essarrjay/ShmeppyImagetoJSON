#!/usr/bin/env python3

#external modules
from PIL import Image
import sys
from pyfiglet import Figlet

#internal modules
import process_image
import menu


def get_max_dim_input():
    dim = -1
    print("-= Maximum map dimension in squares =-")
    while dim <= 0:
        try:
            dim = int(input("Please enter a numerical value of 1 or more (default 50): ") or '50')
        except:
            print("Sorry, let's try that again.\n")
    return dim

def get_palette_size_input():
        ps = -1
        print("-= Palette Size for the Map Image in # of Colors =-")
        while ps <= 0:
            try:
                ps = int(input("Please enter a numerical value of 1 or more (default 4 colors): ") or '4')
            except:
                print("Sorry, let's try that again.\n")
        return ps

def get_process_option():
    option = -1
    filters_map = {2:Image.BOX,3:Image.NEAREST} #uses Image resampling options
    while option <= 0 or option > 2:
        print("-= Process Options =-")
        print("1. Limited Palette\n2. Blended (BOX filter)")
        try:
            option = int(input("Please select a filter option by number (default BOX): ") or '1')
            output = filters_map[option]
        except:
            print("Sorry, please select a option from the menu.\n")
    return output

def process_img_depreciated(image_path,max_map_dim, filter_option):
    #mapsize as a tuple
    map_img = Image.open(image_path)
    map_img.thumbnail((max_map_dim,max_map_dim),resample=filter_option)
    pixels = map_img.convert('RGB').load()
    output_op = Fill_Operation(id='4321')
    for x in range(map_img.width):
        for y in range(map_img.height):
            r,g,b = pixels[x,y]
            output_op.add_pixel(x,y,rgb_to_hex(r,g,b))
    print(output_op.export_json())

def run_depreciated():
    f = Figlet(font='slant')
    print(f.renderText('Shemppy Image\nto JSON'))

    try:
        img_path = sys.argv[1]
    except:
        img_path = input("Image File Path/Name: ")

    process_option = get_process_option()

    max_map_dim = get_max_dim_input()
    print()
    palette_size = get_palette_size_input()
    print()

    fill_op = process_image.image_to_operation(img_path, max_map_dim, palette_size)
    print()
    print(fill_op.export_json())

def run():
    f = Figlet(font='slant')
    print(f.renderText('Shemppy Image\nto JSON'))
    answers = {}
    try:
        img_path = sys.argv[1]
        answers['img_path'] = img_path
    except:
        img_path = False
    answers.update(menu.main(img_path))
    process_option = answers.pop('process_option')
    print(answers)
    fill_op = process_image.image_to_operation(**answers)
    print()
    print(fill_op.export_json())

if __name__ == '__main__':
    run()
