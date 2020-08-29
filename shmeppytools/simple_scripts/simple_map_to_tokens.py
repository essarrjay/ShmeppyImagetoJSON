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


class Token:
    """represents a single shmeppy token"""
    def __init__(
            self, id, type, tokenId, position=(0, 0), color="#FFF",
            label="", width=1, height=1):
        self.id = tokenId
        self.tokenId = tokenId
        self.type = 'CreateToken'
        self.position = position
        self.color = color
        self.label = label
        self.width = width
        self.height = height

    def update(
            self, id=None, type=None, tokenId=None, position=None,
            color=None, label="", width=None, height=None,
            x=None, y=None):
        """updates token properties with any value present"""
        print(f'  UPDATE INFO = P:{position}, C:{color}, L:{label}, W:{width}, H:{height}, X:{x}, Y:{y}')
        if position:
            self.position = position
        if color:
            self.color = color
        if label:
            self.label = label
        if width:
            self.width = width
        if height:
            self.height = height
        if x:
            self.position[0] += x
        if y:
            self.position[1] += y

    def as_op(self):
        """exports the token as a shmeppy compatible operation"""
        out_dict = self.__dict__
        out_dict['position'] = list(out_dict['position'])
        return out_dict


def group_tokens_on_map(maplist, token_padding, group_padding):
    maptokenslist = []
    for map in maplist:
        maptokenslist.append(make_tokens(map))
    tokens_dict = group_tokens(maptokenslist, token_padding, group_padding)
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
        maptokenslist, token_padding, group_padding, align_bottom=True):
    """adjust token positions to group them at the top of the map

    takes a list of token_dicts
    returns a position padded combined token dict
    """
    print("\nRELOCATING TOKENS")
    combined_token_dict = {}
    x = 0
    for token_dict in maptokenslist:
        for id, t in token_dict.items():
            if align_bottom:
                tx, ty = x, -t.height-1
            else:
                tx, ty = x, -1
            t.update(position=(tx, ty))
            x += t.width+token_padding
            combined_token_dict.update({id: t})
        x += group_padding
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
    parser.add_argument("maps", metavar="<map path>", help="Combine each map's tokens into a single output file.", nargs='*')
    parser.add_argument("-c", "--combine", help="Combine each map's tokens into a single output file.", action="store_true")
    parser.add_argument("-sc", "--skipconfirm", help="Skip confirmation prompt for output destination", action="store_true")
    parser.add_argument("-p", "--padding", type=int, default=0, metavar="<integer>", help="Padding between tokens")
    parser.add_argument("-mp", "--mappadding", type=int, default=3, metavar="<integer>", help="Padding between tokens grouped from separate maps")
    parser.add_argument("-d", "--destination", metavar="<path>", help="Output destination path for .json file.")
    args = parser.parse_args()
    print(f'Command Line Arguments, as parsed: {args}')

    # get maps from command line
    try:
        if not args.maps:
            raise Exception("Did not find maps. Please provide below.")
        map_dict = {}
        for p in args.maps:
            print(f"Provided Map Path: {p}")
            temp_p = Path.cwd().joinpath(p)
            print(f"Attempting to import map from: {temp_p.resolve()}")
            map_dict.update({temp_p.stem: import_map(temp_p)})

    # prompt for map if missing from args
    except Exception as e:
        print(e)
        print(f"Looking for maps in: {Path.cwd().resolve()}")
        print("If map is in this folder, just list mapname including")
        print("file extension (.json) otherwise include the folder name")
        print("E.g. mymap.json or backup_maps/mymap.json")
        mpath = input("Please provide relative path to map: ")

        # import maps
        print("Loading Mapfiles:")
        try:
            temp_p = Path.cwd().joinpath(mpath)
            map_dict = {temp_p.stem: import_map(temp_p)}
        except Exception:
            print(f"tried: {Path.cwd().joinpath(mpath)}")
            print("\n\nERROR: File not found, let's try again (or press ctrl+c to quit)\n\n")
            return main()

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
        maplist = map_dict.values()
        output_maps.update({'tokens_map': group_tokens_on_map(maplist, args.padding, args.mappadding)})
    else:
        # process maps separately
        for mname, map in map_dict.items():
            outmap = group_tokens_on_map([map], args.padding, args.mappadding)
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
