#!/usr/bin/env python3

import json
from datetime import datetime
from pathlib import Path
from PIL import Image
import sys

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
            print(f"process_image.py: {result}")
            with export_path.open(mode='w') as json_file:
                json.dump(export_obj,json_file)
        except:
            result = "Error, unable to export."

        return result

def process_img(image_path,mapsize):
    #mapsize as a tuple
    im = Image.open(image_path)
    map_img = im.resize(mapsize)
    pixels = map_img.convert('RGB').load()
    width, height = mapsize
    output_op = Fill_Operation(id='4321')
    for x in range(width):
        for y in range(height):
            r,g,b = pixels[x,y]
            output_op.add_pixel(x,y,rgb_to_hex(r,g,b))
    print(output_op.export_json())

def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def run():
    try:
        img_file = sys.argv[1]
    except:
        img_file = input("Image File Path: ")

    map_x = input("Map horizontal size in pixels (default 50): ")
    map_y = input("Map vertical size in pixels (default 50): ")
    map_x = 50 if map_x == '' else int(map_x)
    map_y = 50 if map_y == '' else int(map_y)

    process_img(img_file,(map_x,map_y))

if __name__ == '__main__':
    run()
