#! usr/bin/env python3
"""collecttokens.py

Fetches tokens from map, returns as compact .json map
"""

# external modules
import json
from pathlib import Path
import argparse

# internal modules
from shmobjs import Token
import uihelper
from shmap import Shmap

BASE_PATH = Path(__file__).resolve().parent
CELL_OPS = {
    'FillCells': ['cellFills'],
    'UpdateCellEdges': ["top", "left"]
    }
TOKEN_OPS = {
    'CreateToken': ['color', 'position', 'tokenId'],
    'MoveToken': ['position', 'tokenId'],
    'UpdateTokenLabel': ['label', 'tokenId'],
    'DeleteToken': ['tokenId'],
    'ResizeToken': ['width', 'height', 'tokenId']
    }
SHMEP_DICT = {"exportFormatVersion": 1, "operations": []}


def group_tokens_on_map(shmaplist, token_padding, group_padding, align='bottom', fillunder=False):
    maptokenslist = []
    for shmap in shmaplist:
        maptokenslist.append(shmap.tokens)
    tokens_dict = group_tokens(maptokenslist, token_padding, group_padding, align)
    ops = tokens_to_ops(tokens_dict, fillunder)
    outshmap = Shmap('outmap', operations=ops)
    return outshmap


def tokens_to_ops(token_dict, fillunder=False):
    """returns a list of ops from a {tokenId:token_obj} dict

    if fillunder == True, drawsfilled cells underneath tokens"""
    outops = []
    for t in token_dict.values():
        outops.append(t.as_op())

        if fillunder:
            fillunder_op = {"id":"underfill", "type":"FillCells", "cellFills":[]}
            x, y = t.position
            for h in range(t.height):
                for w in range(t.width):
                    fillunder_op['cellFills'].append([[x+w, y+h], "#EEE"])
            outops.append(fillunder_op)
    return outops


def group_tokens(
        maptokenslist, token_padding, group_padding, align='bottom'):
    """adjust token positions to group them at the top of the map

    takes a list of token_dicts
    returns a position padded combined token dict
    """
    print("\nRELOCATING TOKENS")

    def get_aligned_pos(alignment, index, token, offset=5):
        """returns updated token position, pos index, based on alignment"""
        i = index
        t = token
        a_dict = {
                'top': (i, -offset, t.width),
                'bottom': (i, -offset-t.height, t.width),
                'left': (-offset, i, t.height),
                'right': (-offset-t.width, i, t.height)
                }
        x, y, delta_i = a_dict[alignment]
        return x, y, i + delta_i

    combined_token_dict = {}
    i = 0
    for token_dict in maptokenslist:
        for id, t in token_dict.items():
            tx, ty, i = get_aligned_pos(align, i, t)
            t.update(position=(tx, ty))
            i += token_padding
            combined_token_dict.update({id: t})
        i += group_padding
    return combined_token_dict


def get_updated_ops(map, offset):
    """for map, offset all draw operations"""
    outops = []
    for op in map['operations']:
        if op['type'] in CELL_OPS.keys():
            pass
        elif op['type'] in TOKEN_OPS.keys():
            pass
    return outops


def export_map(map, outpath):
    """exports map (as dict obj) to outpath"""
    print(f"\nAttempting Export of:\n  {outpath}\n")
    try:
        with outpath.open(mode='w') as j_file:
            json.dump(map, j_file, indent=2)
        result = f"Exported {outpath.name} to:\n  {outpath}"
    except FileNotFoundError:
        result = "Export failed, please enter a valid output destination."
    except SyntaxError as e:
        result = f"Export failed, check that you have entered a valid path name.\n {e}"
    return result

def main():
    """Fetches tokens from map, returns as compact .json map"""
    print(" ===================")
    print("   Token Collector  ")
    print(" ===================")
    print("Press ctrl+c or close window to quit.\n")
    print("Will take any number of .json map files as command line arguments:")
    print(" > map_to_tokens.exe <map-1 path> <map-2 path>...<map-n path>")
    print("    OR")
    print(" > python map_to_tokens.py <map-1 path> <map-2 path>...<map-n path>\n")

    # add arguments to parser
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("maps", metavar="<map path>", help="Combine each map's tokens into a single output file.", nargs='*')
    parser.add_argument("-c", "--combine", help="Combine each map's tokens into a single output file.", action="store_true")
    parser.add_argument("-sc", "--skipconfirm", help="Skip confirmation prompt for output destination", action="store_true")
    parser.add_argument("-p", "--padding", type=int, default=0, metavar="<integer>", help="Padding between tokens")
    parser.add_argument("-mp", "--mappadding", type=int, default=3, metavar="<integer>", help="Padding between tokens grouped from separate maps")
    parser.add_argument("-fu", "--fillunder", help="Place a colored (filled) cell under each token", action="store_true")
    parser.add_argument("-a", "--align", help="Align along which edge of the tokens (when handling tokens larger than 1x1).", choices=['top', 'bottom', 'left', 'right'], default='bottom')
    parser.add_argument("-d", "--destination", metavar="<path>", help="Output destination path for .json file.")
    parser.add_argument("-nep", "--noexitpause", help='Skip "Press Enter to Exit..."', action="store_true")
    args = parser.parse_args()
    print(f'Command Line Arguments, as parsed:\n   {vars(args)}\n')

    # get maps from command line
    shmaps_list = uihelper.get_shmaps(args.maps)

    # set output destination
    outdest = Path(args.destination).resolve() if args.destination else Path.cwd()
    print(f"\nOutput destination currently set to:\n {outdest}")
    if not args.skipconfirm:
        user_outdest = input("Enter to continue, or enter full path to set output destination: ")
        if user_outdest:
            outdest = Path(user_outdest)

    # generate maps
    output_maps = {}
    if args.combine:
        output_maps.update({'tokens_map': group_tokens_on_map(shmaps_list, args.padding, args.mappadding, args.align, args.fillunder)})
    else:
        # process maps separately
        for shmap in shmaps_list:
            outmap = group_tokens_on_map([shmap], args.padding, args.mappadding, args.align, args.fillunder)
            output_maps.update({shmap.name: outmap})

    # save maps to disk
    for name, shmap in output_maps.items():
        print(shmap.export_to(outdest))

    if not args.noexitpause:
        # pause before exiting - necessary for pyinstaller
        input("Press Enter to Exit...")


if __name__ == '__main__':
    main()
