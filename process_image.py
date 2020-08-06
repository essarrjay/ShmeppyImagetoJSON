#external modules
from haishoku.haishoku import Haishoku
from PIL import Image
from os import remove
from math import floor
from pathlib import Path

#internal modules
from palette import *
import shmoperations
import progress_bar

def slice_to_tiles(img_obj,tile_width,tile_height):
    #returns list of image objects as tiles
    tiles = []
    for x in range(0,img_obj.width,tile_width):
        tiles_row = []
        for y in range(0,img_obj.height,tile_height):
            im_crop = img_obj.crop((x,y,x+tile_width,y+tile_height))
            tiles_row.append(im_crop)
        tiles.append(tiles_row)
    return tiles

def get_tile_size(img_obj, max_map_dim):
    #determines tile size, stretching the smaller dimension to match
    w,h = img_obj.size

    if w >= h:
        x_tiles = max_map_dim
        y_tiles = int(round(h / w * max_map_dim))
    else:
        x_tiles = int(round(w / h * max_map_dim))
        y_tiles = max_map_dim

    tile_width = int(w / x_tiles)
    tile_height = int(h / y_tiles)

    print("\n-= Conversion Info =- ")
    print(f'Image Dimensions: {w} x {h} px\n Tile Dimensions: {tile_width} x {tile_height} px\n  Map Dimensions: {x_tiles} x {y_tiles} tiles')

    return (tile_width,tile_height)

def image_to_operation(img_path, max_map_dim, palette_size, debug=False):
    fill_op = shmoperations.Fill_Operation(id='4321')


    palette = get_palette(img_path, palette_size, debug)

    with Image.open(img_path) as im:
        tile_size = get_tile_size(im,max_map_dim)
        tiles_array = slice_to_tiles(im,*tile_size)
        temp_path = 'temp_img.png'
        x, y = 0,0
        print()
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

if __name__ == '__main__':
    image_to_operation(r"test_im\3x3_test_master.png",3,8,debug=True)
