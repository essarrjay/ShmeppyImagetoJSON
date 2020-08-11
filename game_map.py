#external modules
from haishoku.haishoku import Haishoku
from PIL import Image
from os import remove
from pathlib import Path
from datetime import datetime
from copy import deepcopy
from sys import exit
import json
import os

#internal modules
from palette import *
import shmops
import progress_bar


class Game_Map:
    def __init__(self, img_path, map_size=None, debug=False, name=None):
        print("\n||||| Initializing Game Map |||||\n")
        self.path = Path(img_path)
        try:
            with Image.open(self.path) as im:
                self.img_size = im.size
            print(f"   Input File: {self.path.name}")
        except FileNotFoundError:
            print(f"File {img_path} not found, be sure this includes the full or relative path - the folders containing the file, not just the file's name.\n")
            exit()

        self.name = name if name else self.path.stem
        self.shmeppy_json = {"exportFormatVersion":1,"operations":[]}

        try:
            self.map_size = self.get_map_size(int(map_size))
        except TypeError:
            self.map_size = map_size
        self.max_map_dim = max(self.map_size)
        self.debug = debug

        self.tile_raw_size = self.get_tile_size(show_info="Input Image")

    def get_map_size(self, max_map_dim=None):
        #returns x,y tuple of map size in tiles units
        w, h = self.img_size
        mmd = max_map_dim
        if w >= h:
            x_tiles = mmd
            y_tiles = round(h / w * mmd)
        else:
            x_tiles = round(w / h * mmd)
            y_tiles = mmd

        return (x_tiles, y_tiles)

    def get_tile_size(self, map_size = None, show_info = None):
        #returns a tuple of unrounded tile size
        if not map_size: map_size = self.map_size
        w,h = self.img_size
        x_tiles,y_tiles = map_size

        tile_raw_w = w / x_tiles
        tile_raw_h = h / y_tiles

        if self.debug:
            print(f'Raw tile width: {tile_raw_w}\nRaw tile height: {tile_raw_h}')

        tile_w = int(round(tile_raw_w))
        tile_h = int(round(tile_raw_h))

        if show_info:
            print(f'   Image Size: {w} x {h} px\n   Tile  Size: {tile_w} x {tile_h} px\n   Map   Size: {x_tiles} x {y_tiles} tiles')

            error_w = tile_w - tile_raw_w
            error_h = tile_h - tile_raw_h
            print(f'\n -=ERROR INFO=-\n   Tile Size  Width Error: {round(error_w,4)} px \n   Tile Size Height Error: {round(error_h,4)} px \n   Total  Width Rounding Error: {round(error_w * x_tiles,4)} px \n   Total Height Rounding Error: {round(error_h * y_tiles,4)} px\n')

        return (tile_raw_w,tile_raw_h)

    def slice_to_tiles(self, tile_raw_size=None, show_info=""):
        #returns list of image objects as 2d list.
        if not tile_raw_size: tile_raw_size = self.tile_raw_size
        tile_raw_w,tile_raw_h = tile_raw_size
        tile_w,tile_h = round(tile_raw_w),round(tile_raw_h)
        w,h = self.img_size

        if show_info:
            print(f" ==Slicing {show_info} Tiles==")
            print(f'   Tile raw size: {tile_raw_size[0]} x {tile_raw_size[1]} px\n')

        tiles = []
        true_x, true_y = (0,0)
        with Image.open(self.path) as img_obj:
            for y_px in range(0,h,tile_h):
                tiles_row = []
                y = round(true_y)
                for x_px in range(0,w,tile_w):
                    x = round(true_x)
                    im_crop = img_obj.crop((x,y,x+tile_w,y+tile_h))
                    tiles_row.append(im_crop)
                    true_x += tile_raw_w
                tiles.append(tiles_row)
                true_y += tile_raw_h
                true_x = 0

        return tiles

    def get_palette(self, palette_size, sampling_map_size):
        print("==|Generating Palette|==")
        sample_raw_size = self.get_tile_size(sampling_map_size, show_info="Sample Tiles")
        tiles = self.slice_to_tiles(tile_raw_size=sample_raw_size, show_info="Palette Sample")
        temp_path = Path('temp_img.png')
        data = []

        #iterate through Image Objects, get palettes, combine
        for row in progress_bar.progressbar(tiles, " Processing Image for Palette: ", " Samples Row: ",36):
            for tile in row:
                tile.save(temp_path,"PNG")
                pal = get_palette(temp_path, palette_size, debug=False)
                data += pal
                os.remove(temp_path)

        #remove duplicates
        data = list(dict.fromkeys(data))

        #print palette info
        tile_raw_w,tile_raw_h = sample_raw_size
        x_tiles,y_tiles = sampling_map_size
        print(f'\n -=PALETTE INFO=- \n   Sample Grid: {x_tiles} x {y_tiles} tiles \n   Sample Tile Size: {tile_raw_w} x {tile_raw_h} px \n   Total Palette Size: {len(data)} colors\n')

        return data

    def palette_op(self, palette_size, sample_factor = 4):
        #generates an shmops.fill_operation obj
        print("||||| Initiating Palette Fill Operation |||||")
        fill_op = shmops.Fill_Operation(id='4321')

        tiles = self.slice_to_tiles(show_info="Image to Map")

        sampling_map_size = self.get_map_size(sample_factor)
        #get palette to be used in the process
        palette = self.get_palette(palette_size, sampling_map_size)

        temp_path = 'temp_img.png'
        x, y = 0,0
        for row in progress_bar.progressbar(tiles, "Processing Map: ", " Row: ",36):
            for tile in row:
                if self.debug:
                    temp_path = f'{x}x{y}y_temp_img.png'
                    temp_path = Path('./test_tiles/' + temp_path)
                tile.save(temp_path,"PNG")
                dominant = Haishoku.getDominant(str(temp_path))
                tile_color = nearest_color_from_palette(palette,dominant)
                if self.debug: print(f'Tile Address: {x}, {y} | Tile Color: {tile_color} | Saved to:  {temp_path}')
                fill_op.add_fill(x,y,rgb_to_hex(*tile_color))
                x += 1
            y += 1
            x = 0
        if not self.debug: remove(temp_path)

        return fill_op

    def filter_op(self, filter_option):
        #generates an shmops.fill_operation obj using a resize/filter operation
        print("===||| Initiating Filter-Resize Fill Operation |||===")
        fill_op = shmops.Fill_Operation(id='4321')

        map_img = Image.open(self.path)
        map_img.thumbnail((self.max_map_dim, self.max_map_dim),resample=filter_option)
        pixels = map_img.convert('RGB').load()
        for x in progress_bar.progressbar(range(map_img.width), "Processing: ",width=36):
            for y in range(map_img.height):
                r,g,b = pixels[x,y]
                fill_op.add_fill(x,y,rgb_to_hex(r,g,b))
        return fill_op

    def op_to_json(self, op, data_dir=r'./output_files/'):
        #exports map as shmeppy compatible JSON
        if data_dir[-1] != '/': data_dir += '/'

        #generate export filename and export Path obj
        ts = str(datetime.now())[:-7]
        ts = ts.replace(':','').replace('-','').replace(' ','_')
        ms = self.map_size
        filename = f"{self.name}_{ms[0]}x{ms[1]}_{ts}.json"
        export_path = Path(data_dir + filename)

        export_obj = deepcopy(self.shmeppy_json)
        export_obj["operations"].append(op.__dict__)

        try:
            result_str = f"Exporting mapfile: {str(export_path)}\n"
            with export_path.open(mode='w') as json_file:
                json.dump(export_obj, json_file)
        except Exception as e:
            result_str = f"Error: {str(e)}, unable to export.\n"

        return result_str

if __name__ == '__main__':
    #GM = Game_Map(r"test_im\3x3_test_master.png",map_size=(3,3), debug=True)
    GM = Game_Map(r"test_im\toa_58.png",map_size=(47,58), debug=False)
    op = GM.palette_op(4)
    print(GM.op_to_json(op))
    GM = Game_Map(r"test_im\dragonsmaw.png",max_map_dim=31)
    #GM.op_to_json(GM.filter_op(Image.BOX,debug=True))
