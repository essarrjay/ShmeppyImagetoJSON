#! usr/bin/env python3
"""
collecttokens.py

Fetches tokens from map, returns as compact .json map
"""

# external modules
import json
from pathlib import Path
import argparse
from datetime import datetime
from copy import deepcopy

# internal modules
from shmobjs import Token

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


def group_tokens_on_map(maplist, token_padding, group_padding, align='bottom', fillunder=False):
    maptokenslist = []
    for map in maplist:
        maptokenslist.append(make_tokens(map))
    tokens_dict = group_tokens(maptokenslist, token_padding, group_padding, align)
    ops = tokens_to_ops(tokens_dict, fillunder)
    outmap = deepcopy(SHMEP_DICT)
    outmap['operations'] = ops
    return outmap


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


def make_tokens(map, debug=False):
    """returns a dict of {tokenId:token} from map

    Uses final position of token, and omits deleted tokens
    """
    token_dict = {}
    for op in map['operations']:
        if op['type'] == 'CreateToken':
            print(f"+CREATED TOKEN {op['tokenId']}")
            token_dict.update({op['tokenId']: Token(**op)})
        elif op['type'] == 'DeleteToken':
            token_dict.pop(op['tokenId'])
            print(f"-DELETED TOKEN {op['tokenId']}")
        elif op['type'] in TOKEN_OPS.keys():
            token_obj = token_dict[op['tokenId']]
            print(f"=TOKEN OP {op['type']}")
            if debug:
                print(f'  Token properties before:\n      {token_obj.__dict__}')
            print(f'  OP: {op}')
            token_obj.update(**op)
    return token_dict


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


def import_map(inpath):
    """import json, returns map as dict_obj"""
    with open(inpath) as j_file:
        map_dict = json.load(j_file)
    print(f"Successful Import of Map: {inpath}")
    return map_dict


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

def get_maps(args):
    """returns a dict of {map_name: imported_json}"""
    try:
        if not args.maps:
            raise Exception("Did not find maps. Please provide below.")
        maps_dict = {}
        for p in args.maps:
            print(f"Provided Map Path: {p}")
            temp_p = Path.cwd().joinpath(p)
            print(f"Attempting to import map from: {temp_p.resolve()}")
            maps_dict.update({temp_p.stem: import_map(temp_p)})

    # prompt for map if missing from args
    except Exception as e:
        print(e)
        print(f"Looking for maps in: {Path.cwd()}")
        print("If map is in this folder, just list mapname including")
        print("file extension (.json) otherwise include the folder name")
        print("E.g. mymap.json or backup_maps/mymap.json")
        mpath = input("Please provide relative path to map: ")

        # import maps
        print("Loading Mapfiles:")
        try:
            temp_p = Path.cwd().joinpath(mpath)
            maps_dict = {temp_p.stem: import_map(temp_p)}
        except Exception:
            print(f"tried: {Path.cwd().joinpath(mpath)}")
            print("\n\nERROR: File not found, let's try again (or press ctrl+c to quit)\n\n")
            return main()
    return maps_dict

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

    # maps from command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("maps", metavar="<map path>", help="Combine each map's tokens into a single output file.", nargs='*')
    parser.add_argument("-c", "--combine", help="Combine each map's tokens into a single output file.", action="store_true")
    parser.add_argument("-sc", "--skipconfirm", help="Skip confirmation prompt for output destination", action="store_true")
    parser.add_argument("-p", "--padding", type=int, default=0, metavar="<integer>", help="Padding between tokens")
    parser.add_argument("-mp", "--mappadding", type=int, default=3, metavar="<integer>", help="Padding between tokens grouped from separate maps")
    parser.add_argument("-fu", "--fillunder", help="Place a colored (filled) cell under each token", action="store_true")
    parser.add_argument("-a", "--align", help="Align along which edge of the tokens (when handling tokens larger than 1x1).", choices=['top', 'bottom', 'left', 'right'], default='bottom')
    parser.add_argument("-d", "--destination", metavar="<path>", help="Output destination path for .json file.")
    args = parser.parse_args()
    print(f'Command Line Arguments, as parsed:\n   {vars(args)}\n')

    # get maps from command line
    maps_dict = get_maps(args)

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
        maplist = maps_dict.values()
        output_maps.update({'tokens_map': group_tokens_on_map(maplist, args.padding, args.mappadding, args.align, args.fillunder)})
    else:
        # process maps separately
        for mname, map in maps_dict.items():
            outmap = group_tokens_on_map([map], args.padding, args.mappadding, args.align, args.fillunder)
            output_maps.update({mname: outmap})

    # save maps to disk
    for name, map in output_maps.items():
        ts = str(datetime.now())[:-7]
        ts = ts.replace(':', '').replace('-', '').replace(' ', '_')
        filename = f"{name}_{ts}.json"
        print(export_map(map, outdest.joinpath(filename)))

    # pause before exiting - necessary for pyinstaller
    input("Press Enter to Exit...")


if __name__ == '__main__':
    main()
