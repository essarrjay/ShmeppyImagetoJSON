#!/usr/bin/env python3

#external modules
from PIL import Image
import sys
from pyfiglet import Figlet

#internal modules
import process_image

def get_max_dim_input():
    dim = -1
    print("-= Maximum map dimension in squares =-")
    while dim <= 0:
        try:
            dim = int(input("Please enter a numerical value of 1 or more (default 50): ") or '50')
        except:
            print("Sorry, let's try that again.\n")
    return dim

def get_filter_option():
    option = -1
    filters_map = {1:Image.BOX,2:Image.NEAREST} #uses Image resampling options
    while option <= 0:
        print("-= Filter Options =-")
        print("1. BOX (smooth, but some blur)\n2. NEAREST (crisp, artifacts)\n")
        try:
            option = int(input("Please select a filter option by number (default BOX): ") or '1')
            output = filters_map[option]
        except:
            print("Sorry, please select a option from the menu.\n")
    return output

def get_palette_size_input():
        ps = -1
        print("-= Palette Size for the Map Image in # of Colors =-")
        while ps <= 0:
            try:
                ps = int(input("Please enter a numerical value of 1 or more (default 4 colors): ") or '4')
            except:
                print("Sorry, let's try that again.\n")
        return ps

def run():
    f = Figlet(font='slant')
    print(f.renderText('Shemppy Image\nto JSON'))

    try:
        img_path = sys.argv[1]
    except:
        img_path = input("Image File Path/Name: ")

    max_map_dim = get_max_dim_input()
    print()
    palette_size = get_palette_size_input()
    #filter_option = get_filter_option()
    print()
    fill_op = process_image.image_to_operation(img_path, max_map_dim, palette_size)
    print()
    print(fill_op.export_json())


if __name__ == '__main__':
    run()
