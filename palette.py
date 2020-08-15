from haishoku.haishoku import Haishoku
from sys import exit

def get_palette(img_path, palette_size, debug=False, show_palette=False):
    #returns a list of RGB tuples representing a palette of palette_size numbers of color, by maximum use
    try:
        full_palette = Haishoku.getPalette(str(img_path))
        map_palette = full_palette[:palette_size]
        if show_palette: Haishoku.showPalette(str(img_path))
    except FileNotFoundError:
        print(f"File {img_path} not found, be sure this includes the full or relative path - the folders containing the file, not just the file's name.")
        exit()

    if debug:
        print(f' ► Full Palette (Freq,RGB) = {full_palette}')
        print(f' ► Map Reduced Palette (Freq,RGB) = {map_palette}')

    #return only the RGB values
    return dict(map_palette).values()

def nearest_color_from_palette(palette, in_color):
    #returns nearest RGB color in palette
    out_color = min( palette, key = lambda palette_entry: sum((pe - c) ** 2 for pe, c in zip(palette_entry, in_color)))
    return out_color

def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)
