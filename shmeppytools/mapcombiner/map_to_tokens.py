#! usr/bin/env python3
"""
map_to_tokens

Fetches tokens from map, returns as compact .json map
"""

import json
from pathlib import Path
import argparse
from datetime import datetime
from copy import deepcopy
import token

BASE_PATH = Path(__file__).resolve().parent.parent
#SAME_PATH = Path(__file__).resolve().parent
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


def group_tokens_on_map(map):
    tokens_dict = make_tokens(map[0])
    tokens_dict = group_tokens(tokens_dict)
    ops = tokens_to_ops(tokens_dict)
    outmap = deepcopy(SHMEP_DICT)
    outmap['operations'] = ops
    return outmap


def tokens_to_ops(token_dict):
    """returns a list of ops from a {tokenId:token_obj} dict"""
    outops = []
    for t in token_dict.values():
        outops.append(t.as_op())
    return outops


def make_tokens(map):
    """returns a dict of {tokenId:token} from map

    Uses final position of token, and omits deleted tokens
    """
    token_dict = {}
    for op in map['operations']:
        if op['type'] == 'CreateToken':
            print("=== TOKEN CREATED ===")
            token_dict.update({op['tokenId']: token.Token(**op)})
        elif op['type'] == 'DeleteToken':
            token_dict.pop(op['tokenId'])
            print("=== TOKEN DELETED ===")
        elif op['type'] in TOKEN_OPS.keys():
            token_obj = token_dict[op['tokenId']]
            print(f"=== TOKEN {op['type']} ===")
            print(f'||=> TOKEN BEFORE: {token_obj.__dict__}')
            token_obj.update(**op)
            print(f'||=> token properties AFTER: {token_obj.__dict__}')
    return token_dict


def group_tokens(token_dict, align_bottom=True):
    """adjust token positions to group them at the top of the map"""
    print("\nRELOCATING TOKENS")
    x = 0
    for t in token_dict.values():
        if align_bottom:
            tx, ty = x, -t.height-1
        else:
            tx, ty = x, -1
        t.update(position=(tx, ty))
        x += t.width
    return token_dict

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
    """import json"""
    with open(inpath) as j_file:
        map_dict = json.load(j_file)
    print(f"Successful Import of Map: {inpath}")
    return map_dict


def export_map(map, outpath):
    """exports map to outpath"""
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

    # maps from command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("maps", help="Combine each map's tokens into a single output file.", nargs='*')
    parser.add_argument("-c", "--combine", help="Combine each map's tokens into a single output file.", action="store_true")
    parser.add_argument("-d", "--destination", help="Output destination path for .json file.")
    args = parser.parse_args()
    print(f'args = {args}')

    # maps from command line
    try:
        if not args.maps:
            raise Exception("Did not find maps. Please provide below.")
        map_list = []
        for p in args.maps:
            print(f"Provided Map Path: {p}")
            temp_p = BASE_PATH.joinpath(p)
            print(f"Attempting to import map from: {temp_p}")
            map_list.append(import_map(temp_p))

    except Exception as e:
        print(e)
        print(f"Looking for maps in: {BASE_PATH.resolve()}")
        print("If map is in this folder, just list mapname including")
        print("file extension (.json) otherwise include the folder name")
        print("E.g. mymap.json or backup_maps/mymap.json")
        mpath = input("Please provide relative path to map: ")

        # import maps
        print("Loading Mapfiles:")
        try:
            map_list = [import_map(BASE_PATH.joinpath(mpath))]
        except Exception:
            print(f"tried: {BASE_PATH.joinpath(mpath)}")
            print("\n\nERROR: File not found, let's try again (or press ctrl+c to quit)\n\n")
            return main()
    outdest = Path(args.destination).resolve() if args.destination else BASE_PATH
    print(f"\nOutput destination currently set to:\n {outdest}")
    user_outdest = input("Enter to continue, or enter full path to set output destination: ")
    if user_outdest:
        outdest = Path(user_outdest)

    output_maps = {}
    if args.combine:
        for map in map_list:
            output_maps.update({map.name: group_tokens_on_map(map)})
    else:
        output_maps.update({'tokens_map': group_tokens_on_map(map_list)})

    for name, map in output_maps.items():
        ts = str(datetime.now())[:-7]
        ts = ts.replace(':', '').replace('-', '').replace(' ', '_')
        filename = f"{name}_{ts}.json"
        print(export_map(map, outdest.joinpath(filename)))

    # pause before exiting - necessary for pyinstaller
    input("Press Enter to Exit...")


if __name__ == '__main__':
    main()
