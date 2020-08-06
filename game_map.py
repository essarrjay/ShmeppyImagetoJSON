#external modules
from haishoku.haishoku import Haishoku
from PIL import Image
from os import remove
from math import floor
from pathlib import Path
from datetime import datetime
from copy import deepcopy
from sys import exit
import json

#internal modules
from palette import *
import shmops
import progress_bar

class Game_Map:
    def __init__(self, img_path, max_map_dim):
        self.path = img_path
        self.shmeppy_json = {"exportFormatVersion":1,"operations":[]}
        self.max_map_dim = max_map_dim
        try:
            self.tile_size = self.get_tile_size()
        except FileNotFoundError:
            print(f"File {img_path} not found, be sure this includes the full or relative path - the folders containing the file, not just the file's name.")
            exit()

    def get_tile_size(self):
        #determines tile size, stretching the smaller dimension to match
        with Image.open(self.path) as img_obj:
            w,h = img_obj.size

        mmd = self.max_map_dim

        if w >= h:
            x_tiles = mmd
            y_tiles = int(round(h / w * mmd))
        else:
            x_tiles = int(round(w / h * mmd))
            y_tiles = mmd

        tile_w = int(w / x_tiles)
        tile_h = int(h / y_tiles)

        print("\n-= Import Info =- ")
        print(f'Image Dimensions: {w} x {h} px\n Tile Dimensions: {tile_w} x {tile_h} px\n  Map Dimensions: {x_tiles} x {y_tiles} tiles')

        return (tile_w,tile_h)

    def slice_to_tiles(self):
        #returns list of image objects as tiles
        tiles = []
        tile_w,tile_h = self.tile_size
        with Image.open(self.path) as img_obj:
            for x in range(0,img_obj.width,tile_w):
                tiles_row = []
                for y in range(0,img_obj.height,tile_h):
                    im_crop = img_obj.crop((x,y,x+tile_w,y+tile_h))
                    tiles_row.append(im_crop)
                tiles.append(tiles_row)
        return tiles

    def palette_op(self, palette_size, debug=False):
        fill_op = shmops.Fill_Operation(id='4321')

        palette = get_palette(self.path, palette_size, debug)

        tiles_array = self.slice_to_tiles()
        temp_path = 'temp_img.png'
        x, y = 0,0
        for row in progress_bar.progressbar(tiles_array, "Processing: ",36):
            for tile in row:
                if debug:
                    temp_path = f'{x}x{y}y_temp_img.png'
                    temp_path = str(Path(r'./test_tiles' + temp_path))
                tile.save(temp_path,"PNG")
                dominant = Haishoku.getDominant(temp_path)
                tile_color = nearest_color_from_palette(palette,dominant)
                if debug: print(f'Tile Address: {x}, {y}   |   Tile Color: {tile_color}                    ')
                fill_op.add_fill(x,y,rgb_to_hex(*tile_color))
                y += 1
            x += 1
            y = 0

        remove(temp_path)
        return fill_op

    def filter_op(self, filter_option, debug=False):
        #generates an shmops.fill_operation using a resize/filter operation
        map_img = Image.open(self.path)
        map_img.thumbnail((self.max_map_dim, self.max_map_dim),resample=filter_option)
        pixels = map_img.convert('RGB').load()
        fill_op = shmops.Fill_Operation(id='4321')
        for x in progress_bar.progressbar(range(map_img.width), "Processing: ",36):
            for y in range(map_img.height):
                r,g,b = pixels[x,y]
                fill_op.add_fill(x,y,rgb_to_hex(r,g,b))
        return fill_op

    def op_to_json(self, op, data_dir=r'./output_files/'):
        #exports map as shmeppy compatible JSON
        if data_dir[-1] != '/': data_dir += '/'

        #generate export path
        timestamp_str = str(datetime.now())[:-7].replace(':','').replace(' ','_')
        filename = f'game_map_{timestamp_str}.json'
        export_path = Path(data_dir + filename)

        export_obj = deepcopy(self.shmeppy_json)
        export_obj["operations"].append(op.__dict__)

        try:
            result_str = f"Exporting mapfile to {str(export_path)}"
            with export_path.open(mode='w') as json_file:
                json.dump(export_obj, json_file)
        except Exception as e:
            result_str = f"Error: {str(e)}, unable to export."

        return result_str

if __name__ == '__main__':
    GM = Game_Map(r"est_im\3x3_test_master.png",max_map_dim=3)
    op = GM.palette_op(4,debug=True)
    print(GM.op_to_json(op))
    #GM = Game_Map(r"test_im\dragonsmaw.png",max_map_dim=31)
    #GM.op_to_json(GM.filter_op(Image.BOX,debug=True))
