from haishoku.haishoku import Haishoku

def get_palette(img_path, palette_size):
    #gets a palette of palette_size number of color, by maximum use
    full_palette = Haishoku.getPalette(img_path)[:palette_size]
    return dict(full_palette).values()

def nearest_color_from_palette(palette, in_color):
    #returns nearest RGB color in palette
    out_color = min( palette, key = lambda palette_entry: sum((pe - c) ** 2 for pe, c in zip(palette_entry, in_color)))
    return out_color
