from PyInquirer import prompt, Separator
from pyfiglet import Figlet
import sys

global answers
questions = [
    {
        'type': 'list',
        'name': 'process_option',
        'message': '-= How would you like to process this image? =-',
        'choices': [
            'Limited Palette',
            'Blended (BOX filter)',
            Separator(),
            'Learn MOre'
        ],
        'default': 'Limited Palette',
        'filter': lambda val: val.lower()
    },
    {
        'type': 'input',
        'name': 'max_map_dim',
        'message': '-= Maximum map dimension in squares: ',
        'filter': lambda val: int(val)
    },
    {
       'type': 'input',
        'name': 'palette_size',
        'message': '-= Palette Size for the Map Image in # of Colors (8 max): ',
        'default': '4',
        'filter': lambda val: int(val),
        'when': lambda answers: answers['process_option'] == 'limited palette'
    },
    {
       'type': 'confirm',
        'name': 'debug',
        'message': 'Debug Mode? ',
        'default': False,
        #'filter': lambda val: bool(val),
        #'when': lambda answers: answers['process_option'] == 'limited palette'
    }

]

image_file_question = {
    'type': 'input',
    'name': 'img_path',
    'message': '-= Image File Path/Name: '}

def check_for_filename():
    global questions
    questions = [image_file_question, *questions]

def main(have_file=False):
    if not have_file: check_for_filename()
    answers = prompt(questions)
    #print(answers)
    return(answers)

if __name__ == '__main__':
    main()
