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

    def export_json(self, filename, data_dir=r'./'):
        """Exports the Fill_Operation data as shmeppy friendly JSON"""
        if data_dir[-1] != '/': data_dir += '/'

        #generate export path
        export_path = Path(data_dir + filename)
        export_obj["operations"].append(self.__dict__)

        try:
            result = f"Exporting mapfile to {str(export_path)}"
            with export_path.open(mode='w') as json_file:
                json.dump(export_obj,json_file)
        except:
            result = "Error, unable to export."

        return result

def process_img(image_path,map_major_dim, filter_option):
    #mapsize as a tuple
    try:
        map_img = Image.open(image_path)
    except:
        print(f"File {image_path} not found, be sure this includes the full or relative path - the folders containing the file, not just the file's name.\n")
    map_img.thumbnail((map_major_dim,map_major_dim),resample=filter_option)
    pixels = map_img.convert('RGB').load()
    output_op = Fill_Operation(id='4321')
    w,h = im.size
    for x in range(w):
        for y in range(h):
            r,g,b = pixels[x,y]
            output_op.add_pixel(x,y,rgb_to_hex(r,g,b))

    #set filename
    ts = str(datetime.now())[:-7]
    ts = ts.replace(':','').replace('-','').replace(' ','_')
    filename = f"{image_path.stem}_{w}x{h}_{ts}.json"

    result = output_op.export_json(filename)
    return result

def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def get_max_dim_input():
    dim = -1
    print("-= Map major (max) dimension in squares =-")
    while dim <= 0:
        try:
            dim = int(input("Please enter a numerical value of 1 or more (default 24): ") or '24')
        except:
            print("Sorry, let's try that again.\n")
    return dim

def get_filter_option():
    option = -1
    filters_map = {1:Image.BOX,2:Image.NEAREST,3:Image.LANCZOS} #uses Image resampling options
    while option <= 0:
        print("-= Filter Options =-")
        print("1. BOX (smooth, but some blur)\n2. NEAREST (crisp, artifacts)\n3. LANCZOS (smoothest, but slowest to process)")
        try:
            option = int(input("Please select a filter option by number (default BOX): ") or '1')
            return filters_map[option]
        except:
            print("Sorry, please select a option from the menu.\n")


def simple_title():
    lines = ["\n"]
    lines += ["==============================="]
    lines += ["Convert an Image to Shmeppy Map"]
    lines += ["==============================="]
    lines += ["\n"]
    return "\n".join(lines)

def main():
    print(simple_title())

    try:
        img_file = sys.argv[1]
    except:
        img_file = input("Image File Path/Name: ")

    map_major_dim = get_max_dim_input()
    print()
    filter_option = get_filter_option()
    print()
    process_img(img_file,map_major_dim, filter_option)
    input("Press Enter to Quit...")

if __name__ == '__main__':
    main()
