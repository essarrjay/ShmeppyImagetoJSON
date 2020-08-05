#!/usr/bin/env python3

import json
from datetime import datetime
from pathlib import Path
from PIL import Image
import sys
from pyfiglet import Figlet

export_obj = {"exportFormatVersion":1,"operations":[]}

class Fill_Operation:
    def __init__(self, id='', type='FillCells'):
        self.id = id
        self.type = type
        self.cellFills = []

    def add_pixel(self,x_coord,y_coord,color):
        coordinates = [x_coord,y_coord]
        pixel_data = [coordinates,color]
        self.cellFills.append(pixel_data)

    def export_json(self, data_dir=r'./'):
        #exports table_data as JSON
        if data_dir[-1] != '/': data_dir += '/'

        #generate export path
        timestamp_str = str(datetime.now())[:-7]
        timestamp_str = timestamp_str.replace(':','').replace(' ','_')
        filename = f'game_map_{timestamp_str}.json'
        export_path = Path(data_dir + filename)
        export_obj["operations"].append(self.__dict__)

        try:
            result = f"Exporting mapfile to {str(export_path)}"
            with export_path.open(mode='w') as json_file:
                json.dump(export_obj,json_file)
        except:
            result = "Error, unable to export."

        return result

def process_img(image_path,max_map_dim, filter_option):
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

def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

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

def run():
<<<<<<< HEAD
    f = Figlet(font='slant')
    print(f.renderText('Shemppy Image\nto JSON'))
=======
    f = Figlet(font='larry3d')
    print(f.renderText('Shemppy Map Maker'))
>>>>>>> 502c8325e21b78f10f5cda60489a2189f8a8eebf

    try:
        img_file = sys.argv[1]
    except:
        img_file = input("Image File Path/Name: ")

    max_map_dim = get_max_dim_input()
    print('\n')
    filter_option = get_filter_option()
    print('\n')
    process_img(img_file,max_map_dim, filter_option)
    print('\n')

if __name__ == '__main__':
    run()
