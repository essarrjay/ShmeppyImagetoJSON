from haishoku.haishoku import Haishoku
from sys import exit

def get_palette(img_path, palette_size, freq_min=None, debug=False, show_palette=False):
    """returns a list of RGB tuples representing a palette of palette_size numbers of color, by maximum use"""

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
        print(f' ► Autopalette threshold = {freq_min}')

    if freq_min:
        output = []
        if map_palette[0][0] < freq_min:
            #return dominant color if no colors exceed threshold
            output = [map_palette[0][1]]
            print('  =Sample Warning: ')
            print(f'   No color exceeds in {round(freq_min*100,1)}% sample tile. Color {output[0]} represents highest porportion of sample ({map_palette[0][0]*100}%) and will be used as result.')
        else:
            #filter colors below freq_min
            for freq,rgb in map_palette:
                if freq >= freq_min:
                    output.append(rgb)
        if debug: print(f' ► Sample tile palette length: {len(output)}')

    else:
        #return only the RGB values
        output = dict(map_palette).values()

    return output

def nearest_color_from_palette(palette, in_color):
    """returns nearest RGB color in palette"""
    out_color = min( palette, key = lambda palette_entry: sum((pe - c) ** 2 for pe, c in zip(palette_entry, in_color)))
    return out_color

def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)
