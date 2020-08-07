from PyInquirer import prompt, Separator
from pyfiglet import Figlet
import sys

global answers
questions = [
    {
        'type': 'list',
        'name': 'op_type',
        'message': '-= How would you like to process this image? =-',
        'choices': [
            'Palette - sharp tiles, slow',
            'Filter resize - faster, blended tiles',
            Separator(),
            'Help: Learn More',
            'Exit'
        ],
        'default': 'Palette',
        'filter': lambda val: val.lower()
    },
    {
        'type': 'list',
        'name': 'filter_type',
        'message': '-= Which filter would you like to use? =-',
        'choices': [
            'NEAREST - sharp tiles, some artifacts',
            'BOX - idential weight',
            'BILINEAR - linear interpolation',
            'HAMMING - sharper than BILINEAR, less distortion than BOX',
            'BICUBIC - cubic interpolation',
            'LANCZOS - trucated sinc',
        ],
        'default': 'BOX',
        'filter': lambda val: lookup_filter(val.lower()),
        'when': lambda answers: answers['op_type'].startswith('fil')
    },
    {
        'type': 'input',
        'name': 'max_map_dim',
        'message': '-= Maximum map dimension in squares: ',
        'default': '23',
        'filter': lambda val: int(val),
        'when': lambda answers: check_for_continue(answers)
    },
    {
       'type': 'input',
        'name': 'palette_size',
        'message': '-= Palette Size for the Map Image in # of Colors (8 max): ',
        'default': '4',
        'filter': lambda val: int(val),
        'when': lambda answers: answers['op_type'].startswith('pal')
    },
    {
       'type': 'confirm',
        'name': 'debug',
        'message': 'Debug Mode? ',
        'default': False,
        'when': lambda answers: check_for_continue(answers)
    }

]

image_file_question = {
    'type': 'input',
    'name': 'img_path',
    'message': '-= Image File Path/Name: '}

def check_for_continue(answers):
    r = answers['op_type'].startswith('exit') or answers['op_type'].startswith('help')
    return not r

def check_for_filename():
    global questions
    questions = [image_file_question, *questions]

def lookup_filter(val):
    f = val.split()[0]
    filter_dict = {"bicubic":Image.BICUBIC, "bilinear":Image.BILINEAR, "box":Image.BOX, "hamming":Image.HAMMING, "lanczos":Image.LANCZOS, "nearest":Image.NEAREST, }
    return filter_dict[f]

def main(have_file=False):
    if not have_file: check_for_filename()
    answers = prompt(questions)
    #print(answers)
    return(answers)

if __name__ == '__main__':
    main()
