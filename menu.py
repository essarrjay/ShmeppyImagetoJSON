from PyInquirer import prompt, Separator
from pyfiglet import Figlet
from PIL import Image

start = [
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
]

questions = [
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
        'name': 'map_dim_x',
        'message': '-= Map Dimension in X Direction: ',
        'default': '47',
        'filter': lambda val: int(val),
    },
    {
        'type': 'input',
        'name': 'map_dim_y',
        'message': '-= Map Dimension in Y Direction: ',
        'default': '58',
        'filter': lambda val: int(val),
    },
    {
       'type': 'input',
        'name': 'sample_factor',
        'message': f'-= Palette sample maximum map dimension (integer): ',
        'default': '4',
        'filter': lambda val: int(val),
        'when': lambda answers: answers['op_type'].startswith('pal')
    },
    {
       'type': 'input',
        'name': 'palette_size',
        'message': '-= Number of Palette Colors to Return per Sample (8 max): ',
        'default': '8',
        'filter': lambda val: int(val),
        'when': lambda answers: answers['op_type'].startswith('pal')
    },
    {
       'type': 'confirm',
        'name': 'debug',
        'message': 'Debug Mode? ',
        'default': False,
    }

]

image_file_question = {
    'type': 'input',
    'name': 'img_path',
    'message': '-= Image File Path/Name: '}

def is_not_process(answers):
    return True if answers['op_type'].startswith('exit') or answers['op_type'].startswith('help') else False

def lookup_filter(val):
    f = val.split()[0]
    filter_dict = {"bicubic":Image.BICUBIC, "bilinear":Image.BICUBIC, "box":Image.BOX, "hamming":Image.HAMMING, "lanczos":Image.LANCZOS, "nearest":Image.NEAREST}
    return filter_dict[f]

def main(have_file=False):
    if not have_file:
        global start
        start = [image_file_question, *start]
    answers = prompt(start)
    if is_not_process(answers): return answers
    answers.update(prompt(questions, answers))
    #answers['sample_factor'] = min(answers['sample_factor'],answers['max_map_dim'])
    return answers

if __name__ == '__main__':
    main()
