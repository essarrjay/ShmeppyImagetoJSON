import cutie
from sys import exit
from pathlib import Path
from PIL import Image

def main_menu(img_path=None):
    print("\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
    print("  Image to Shmeppy JSON Converter ")
    print("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
    answers={'img_path':img_path, 'map_dim_y':None}
    if not img_path:
        answers['img_path'] = input("-= Image File Path/Name: ")
    # Get the op_type
    print("-= How would you like to process this image? =-")
    # List of op_types to select from, including some captions
    op_types = ['Palette - sharp tiles, slow',
        'Filter resize - faster, blended tiles',
        '------',
        'Help: Learn More',
        'Exit']
    # List entries which are captions and thus not selectable
    captions = [2]
    answers['op_type'] = op_types[
        cutie.select(op_types, caption_indices=captions,caption_prefix="   ")].lower()

    if answers['op_type'].startswith('exit'):
        exit()

    elif answers['op_type'].startswith('help'):
        p = Path("help.txt")
        with open(p, encoding="utf8") as ht:
            print(ht.read())
        return main_menu(img_path = answers['img_path'])

    print()
    #prompt map dimensions or fetch major dimension
    answers['autoscale'] = cutie.prompt_yes_or_no('Autoscale with the map\'s major dimension?',yes_text="Yes, autoscale", no_text="No, I will provide two dimensions", default_is_yes=True)
    answers.update(map_size_menu(answers['autoscale']))

    if answers['op_type'].startswith('fil'):
        answers.update(filter_menu())

    elif answers['op_type'].startswith('pal'):
        answers.update(palette_menu())

    print()
    answers['debug'] = cutie.prompt_yes_or_no('Debug Mode? ')

    return answers

def map_size_menu(autoscale=True):
    response = {}
    if autoscale:
        response['map_major_dim'] = cutie.get_number(
            '-= Map Major Dimension:',
            min_value=1,
            max_value=999,
            allow_float=False)
    else:
        response['map_dim_x'] = cutie.get_number(
            '-= Map Dimension - Horizontal:',
            min_value=1,
            max_value=999,
            allow_float=False)

        response['map_dim_y'] = cutie.get_number(
            '-= Map Dimension -   Vertical:',
            min_value=1,
            max_value=999,
            allow_float=False)
    return response

def filter_menu():
    response = {}
    print('\n-= Which filter would you like to use? =-')
    choices = ['NEAREST - sharp tiles, some artifacts','BOX - idential weight','BILINEAR - linear interpolation','HAMMING - sharper than BILINEAR, less distortion than BOX','BICUBIC - cubic interpolation','LANCZOS - trucated sinc']
    val = choices[cutie.select(choices,selected_index=1)].lower()
    response['filter_type'] = lookup_filter(val)

    return response

def palette_menu():
    response = {}
    print()

    response['sample_factor'] = cutie.get_number(
        '-= Sample grid major dimension (integer):',
        min_value=1,
        max_value=999,
        allow_float=False)

    response['palette_size'] = cutie.get_number(
        '-= Number of Palette Colors to Return per Sample (8 max, enter 0 for automatic selection):',
        min_value=0,
        max_value=8,
        allow_float=False)

    response['palette_rescale'] = cutie.prompt_yes_or_no('-= Rescale Image before palette sample (reduces processing time)?',yes_text="Yes, rescale", no_text="No, use original image dimensions", default_is_yes=True)

    return response

def lookup_filter(val):
    f = val.split()[0]
    filter_dict = {"bicubic":Image.BICUBIC, "bilinear":Image.BICUBIC, "box":Image.BOX, "hamming":Image.HAMMING, "lanczos":Image.LANCZOS, "nearest":Image.NEAREST}
    return filter_dict[f]

if __name__ == '__main__':
    print(main_menu())
