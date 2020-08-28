#external modules
from haishoku.haishoku import Haishoku
from PIL import Image
from pathlib import Path
from datetime import datetime
from copy import deepcopy
from sys import exit
import json

#internal modules
from palette import *
import shmops
import progress_bar
import shmobjs

#init globals
BASE_DIR = Path(__file__).resolve().parent
config_path = BASE_DIR.joinpath('config.json')
with open(config_path) as f:
    config_dict = json.load(f)
AUTOPAL_THRESHOLD = config_dict["autopalette_threshold"]
SHMEPPY_JSON = { "exportFormatVersion":1,"operations":[]}

class Game_Map:
    """Represents all data needed to create shmeppy game maps.

    Attributes
    ----------
    debug : boolean
        flags additional outputs
    path : pathlib.Path obj
        points to input image file
    img_size : (int,int)
        x,y dimensions of image at path, in px
    name : str
        name of map, pulled from image file if not provided
    map_size : (int,int)
        x,y dimensions of output map in squares
    map_major_dim : int
        largest dimension of map_size (in squares)
    tile_raw_size : (float,float)
        dimensions of each tile in px. tiles are an area of input image representing a single output square of the Shmeppy map.
    """

    def __init__(self, img_path, map_size=None, debug=False, name=None):
        print("\n||||| Initializing Game Map |||||\n")

        self.debug = debug
        dbset = "ON" if debug is True else "OFF"
        print(f' ► Debug mode is {dbset}')

        self.path = Path(img_path)
        try:
            with Image.open(self.path) as im:
                self.img_size = im.size
            print(f"   Input File: {self.path.name}")
        except FileNotFoundError:
            print(f"File \"{img_path}\" not found, be sure this includes the full or relative path - the folders containing the file, not just the file's name.\n")
            exit()

        self.name = name if name else self.path.stem

        try:
            self.map_size = self.get_map_size(int(map_size))
        except TypeError:
            self.map_size = map_size

        self.map_major_dim = max(self.map_size)
        self.tile_raw_size = self.get_tile_size(show_info="Input Image")

    def get_map_size(self, map_major_dim=None):
        """Returns x,y tuple of map size in tiles units"""
        w, h = self.img_size
        mmd = map_major_dim
        if w >= h:
            x_tiles = mmd
            y_tiles = round(h / w * mmd)
        else:
            x_tiles = round(w / h * mmd)
            y_tiles = mmd

        return (x_tiles, y_tiles)

    def get_tile_size(self, map_size = None, show_info = None):
        """Returns a tuple of unrounded tile size"""
        if not map_size: map_size = self.map_size
        w,h = self.img_size
        x_tiles,y_tiles = map_size

        tile_raw_w = w / x_tiles
        tile_raw_h = h / y_tiles

        if self.debug:
            print(f' ► Raw tile width: {tile_raw_w}\n ► Raw tile height: {tile_raw_h}')

        tile_w = int(round(tile_raw_w))
        tile_h = int(round(tile_raw_h))

        if show_info:
            print(f'   Image Size: {w} x {h} px\n   Tile  Size: {tile_w} x {tile_h} px\n   Map   Size: {x_tiles} x {y_tiles} tiles')

            error_w = tile_w - tile_raw_w
            error_h = tile_h - tile_raw_h
            print(f'\n -=ERROR INFO=-\n   Tile Size  Width Error: {round(error_w,4)} px \n   Tile Size Height Error: {round(error_h,4)} px \n   Total  Width Rounding Error: {round(error_w * x_tiles,4)} px \n   Total Height Rounding Error: {round(error_h * y_tiles,4)} px\n')

        return (tile_raw_w,tile_raw_h)

    def slice_to_tiles(self, tile_raw_size=None, show_info=""):
        """Returns list of image objects as 2d list"""
        if not tile_raw_size: tile_raw_size = self.tile_raw_size
        tile_raw_w,tile_raw_h = tile_raw_size
        tile_w,tile_h = round(tile_raw_w),round(tile_raw_h)

        if show_info:
            print(f" ==Slicing {show_info} Tiles==")
            print(f'   Tile raw size: {tile_raw_size[0]} x {tile_raw_size[1]} px\n')

        #process into list of image objects
        tiles = []
        true_x, true_y = (0,0)
        with Image.open(self.path) as img_obj:
            w,h = img_obj.size
            for row in range(0,h-tile_h,tile_h):
                tiles_row = []
                y = round(true_y)
                for col in range(0,w-tile_w,tile_w):
                    x = round(true_x)
                    im_crop = img_obj.crop((x,y,x+tile_w,y+tile_h))
                    tiles_row.append(im_crop)
                    true_x += tile_raw_w
                tiles.append(tiles_row)
                true_y += tile_raw_h
                true_x = 0

        return tiles

    def get_combined_palette(self, palette_size, sampling_map_size):
        """Returns a combined list of RGB colors from sampled map slices"""
        print("==|Generating Palette|==")
        sample_raw_size = self.get_tile_size(sampling_map_size, show_info="Sample Tiles")
        tiles = self.slice_to_tiles(tile_raw_size=sample_raw_size, show_info="Palette Sample")
        temp_path = Path('temp_img.png')
        data = []

        #set autopalette values
        if palette_size == 0:
            freq_min = AUTOPAL_THRESHOLD
            palette_size = 8
        else:
            freq_min = None

        #iterate through Image Objects, get palettes, combine
        for row in progress_bar.progressbar(tiles, " Processing Image for Palette: ", " Samples Row: ",36):
            for tile in row:
                tile.save(temp_path,"PNG")
                pal = get_palette(temp_path, palette_size, freq_min=freq_min, debug=self.debug)
                data += pal
                temp_path.unlink()

        #remove duplicates
        data = list(dict.fromkeys(data))

        #print palette info
        tile_raw_w,tile_raw_h = sample_raw_size
        x_tiles,y_tiles = sampling_map_size
        print(f'\n -=PALETTE INFO=- \n   Sample Grid: {x_tiles} x {y_tiles} tiles \n   Sample Tile Size: {tile_raw_w} x {tile_raw_h} px \n   Total Palette Size: {len(data)} colors\n')

        return data

    def palette_op(self, palette_size, sample_factor = 4):
        """Generates an shmops.fill_operation obj"""
        print("||||| Initiating Palette Fill Operation |||||")
        fill_op = shmops.Fill_Operation(id='4321')

        tiles = self.slice_to_tiles(show_info="Image to Map")

        #get palette to be used in the process
        if sample_factor == 1:
            palette = get_palette(self.path, palette_size, debug=self.debug)
        else:
            #get combined palette by slicing map into sample tiles
            sampling_map_size = self.get_map_size(sample_factor)
            palette = self.get_combined_palette(palette_size, sampling_map_size)

        temp_path = Path('temp_img.png')
        x, y = 0,0
        for row in progress_bar.progressbar(tiles, "Processing Map: ", " Row: ",36):
            for tile in row:
                #if self.debug:
                #    temp_path = f'{x}x{y}y_temp_img.png'
                #    temp_path = Path('./test_tiles/' + temp_path)
                tile.save(temp_path,"PNG")
                dominant = Haishoku.getDominant(str(temp_path))
                tile_color = nearest_color_from_palette(palette,dominant)
                #if self.debug: print(f'Tile Address: {x}, {y} | Tile Color: {tile_color} | Saved to:  {temp_path}')
                fill_op.add_fill(x,y,rgb_to_hex(*tile_color))
                x += 1
            y += 1
            x = 0
        if not self.debug: temp_path.unlink()

        return fill_op

    def filter_op(self, filter_option):
        """Returns a shmops.fill_operation obj using a resize/filter operation"""
        print("===||| Initiating Filter-Resize Fill Operation |||===")
        fill_op = shmops.Fill_Operation(id='4321')

        with Image.open(self.path) as map_img:
            map_img.thumbnail((self.map_major_dim, self.map_major_dim),resample=filter_option)
            pixels = map_img.convert('RGB').load()
            for x in progress_bar.progressbar(range(map_img.width), "Processing: ",width=36):
                for y in range(map_img.height):
                    r,g,b = pixels[x,y]
                    fill_op.add_fill(x,y,rgb_to_hex(r,g,b))
        return fill_op

    def token_op(self, filter_option):
        """Returns a list of token ops using a resize/filter operation"""
        print("===||| Initiating Image to Token Operation |||===")
        token_ops = []
        with Image.open(self.path) as map_img:
            map_img.thumbnail((self.map_major_dim, self.map_major_dim),resample=filter_option)
            pixels = map_img.convert('RGB').load()
            for x in progress_bar.progressbar(range(map_img.width), "Processing: ",width=36):
                for y in range(map_img.height):
                    r,g,b = pixels[x,y]
                    id = str(x)+"."+str(y)
                    t = shmobjs.Token(id=id, tokenId=id, position=(x,y), color=rgb_to_hex(r,g,b))
                    token_ops.append(t.as_op())
        return token_ops

    def op_to_json(self, op, out_dir=r'./output_files/'):
        """Exports Fill_Operation as shmeppy compatible JSON"""

        #generate export filename and export Path obj
        ts = str(datetime.now())[:-7]
        ts = ts.replace(':','').replace('-','').replace(' ','_')
        ms = self.map_size
        filename = f"{self.name}_{ms[0]}x{ms[1]}_{ts}.json"
        export_path = Path(out_dir).joinpath(filename)

        export_obj = deepcopy(SHMEPPY_JSON)
        export_obj["operations"].append(op.__dict__)

        try:
            result_str = f"Exporting mapfile: {str(export_path)}\n"
            with export_path.open(mode='w') as json_file:
                json.dump(export_obj, json_file)
        except Exception as e:
            result_str = f"Error: {str(e)}, unable to export.\n"

        return result_str

if __name__ == '__main__':
    GM = Game_Map(r"test_im\dragonsmaw.png",map_size=(31))
    op = GM.palette_op(4)
    print(GM.op_to_json(op))
    GM.op_to_json(GM.filter_op(Image.BOX,debug=True))
    print(GM.op_to_json(op))
