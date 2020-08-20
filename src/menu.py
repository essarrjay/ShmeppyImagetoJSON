import cutie
from sys import exit
from pathlib import Path
from PIL import Image

#internal modules
import combine_maps

#set menu interface
#select
DESEL_P: str = '\033[1m [ ]\033[0m '
SEL_P: str = '\033[1m [\033[32;1mx\033[0;1m]\033[0m '
#confirm
DECON_P: str = '   '
CON_P: str = '\033[1m >\033[0m '

def main_menu(img_path=None):
    print()
    print("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
    print("  Image to Shmeppy JSON Converter ")
    print("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")

    #initialize answers
    answers={'img_path':img_path, 'map_dim_y':None}

    # Get the op_type
    print("    ==MENU OPTIONS==")

    # List of op_types to select from, including some captions
    op_types = ['1. Convert Image to Shmeppy .json file using:',
        'Palette - sharp tiles, slow',
        'Filter resize - faster, blended tiles',
        '   --------',
        '2. Merge',
        'Shmeppy .json files',
        '   --------',
        '3. Other',
        'Help: Learn More',
        'Exit']
    captions = [0,3,4,6,7]

    answers['op_type'] = op_types[
        cutie.select(op_types, caption_indices=captions,caption_prefix="", selected_prefix=SEL_P,deselected_prefix=DESEL_P)].lower()

    #check for early exits
    if answers['op_type'].startswith('exit'):
        exit()
    elif answers['op_type'].startswith('help'):
        base_dir = Path(__file__).resolve().parent
        p = base_dir.joinpath("help.txt")
        with open(p, encoding="utf8") as ht:
            print(ht.read())
        return main_menu()
    elif answers['op_type'].startswith('shm'):
        combine_maps.main()
        exit()

    #check for image path
    if not img_path:
        answers['img_path'] = input("-= Image File Path/Name: ")

    print()
    #prompt process type questions
    if answers['op_type'].startswith('fil'):
        answers.update(filter_menu())

    elif answers['op_type'].startswith('pal'):
        answers.update(palette_menu())

    print()
    answers['debug'] = cutie.prompt_yes_or_no('Debug Mode? ',   selected_prefix=CON_P, deselected_prefix=DECON_P)

    print()
    #confirm to proceed
    answers['confirm'] = cutie.prompt_yes_or_no('Proceed with Processing? ', default_is_yes=True,  selected_prefix=CON_P, deselected_prefix=DECON_P)
    if not answers['confirm']:
        print("Processing terminated, exiting program.")
        exit()

    return answers

def convert_shared_menu():
    """shared prompts for all image conversion menus"""
    response = {}
    response['autoscale'] = cutie.prompt_yes_or_no('Autoscale with the map\'s major dimension?',yes_text="Yes, autoscale", no_text="No, I will provide two dimensions", default_is_yes=True, selected_prefix=CON_P, deselected_prefix=DECON_P)

    print()
    response.update(map_size_menu(response['autoscale']))

    return response

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
    response = convert_shared_menu()
    print('-= Which filter would you like to use? =-')
    choices = ['NEAREST - sharp tiles, some artifacts','BOX - idential weight','BILINEAR - linear interpolation','HAMMING - sharper than BILINEAR, less distortion than BOX','BICUBIC - cubic interpolation','LANCZOS - trucated sinc']
    val = choices[cutie.select(choices,selected_index=1)].lower()
    response['filter_type'] = lookup_filter(val)

    return response

def palette_menu():
    response = convert_shared_menu()

    response['sample_factor'] = cutie.get_number(
        '-= Sample grid major dimension (integer):',
        min_value=1,
        max_value=999,
        allow_float=False)

    print()
    response['palette_size'] = cutie.get_number(
        '-= Number of Palette Colors to Return per Sample (8 max, enter 0 for automatic selection):',
        min_value=0,
        max_value=8,
        allow_float=False)

    print()
    response['palette_rescale'] = cutie.prompt_yes_or_no('-= Rescale Image before palette sample (reduces processing time)?',yes_text="Yes, rescale", no_text="No, use original image dimensions", default_is_yes=True)

    return response

def lookup_filter(val):
    f = val.split()[0]
    filter_dict = {"bicubic":Image.BICUBIC, "bilinear":Image.BICUBIC, "box":Image.BOX, "hamming":Image.HAMMING, "lanczos":Image.LANCZOS, "nearest":Image.NEAREST}
    return filter_dict[f]

if __name__ == '__main__':
    print(main_menu())
