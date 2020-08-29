#! usr/bin/env python3

# external modules
import json
from pathlib import Path
from collections import Counter
import sys
from datetime import datetime

# internal modules
from shmap import Shmap

PADDING = 10
BASE_PATH = Path(__file__).resolve().parent
CELL_OPS = {'FillCells': ['cellFills'], 'UpdateCellEdges': ["top", "left"]}
OTHER_OPS = {'CreateToken': ['color', 'position']}
SHMEP_DICT = {"exportFormatVersion": 1, "operations": []}


def fillcells_xys(action):
    """returns lists of x,y coords"""

    x_list = []
    y_list = []
    for cell in action:
        x, y = cell[0]
        x_list.append(x)
        y_list.append(y)
    return x_list, y_list


def get_new_corners(bb1, bb2):
    """returns tuple of corners describing box bounding two bounding boxes"""
    (ux1, uy1), (lx1, ly1) = bb1
    (ux2, uy2), (lx2, ly2) = bb2
    ul_corner = min(ux1, ux2), min(uy1, uy2)
    lr_corner = max(lx1, lx2), max(ly1, ly2)
    return ul_corner, lr_corner


def count_ops(map):
    print("................")
    print("Operations Count")
    print("................")
    op_list = []
    for op in map['operations']:
        op_list.append(op['type'])
    for k, v in Counter(op_list).most_common():
        print(f'{k} : {v}')


def combine_maps(map_list, layout=(0, 1), padding=0):
    """combine maps in map_list with padding"""
    total_x, total_y = 0, 0
    h, v = layout
    layout = {}
    for map in map_list:
        bb = map.set_bounding_box()
        print(f"bounding boxes = {bb}")
        mapdim = map.get_bb_dimensions()
        print(f"map dimensions = {mapdim}")

        # create relative placement of map
        x = total_x-bb[0][0]
        y = total_y-bb[0][1]

        layout.update({(x, y): (map, mapdim)})

        # set next map's coordinates
        total_x += (mapdim[0]+padding)*h
        total_y += (mapdim[1]+padding)*v

    print(" +++++++++++++++++++++++++++++++")
    print("  Writing New Drawing Operations")
    print(" +++++++++++++++++++++++++++++++")

    # offset maps
    outmap = Shmap('outmap')
    print(f"shmap ops: {outmap.operations}")
    for offset, (map, mapdim) in layout.items():
        print(f"Map {map.name} of size {mapdim[0]}x{mapdim[1]} being offset by x,y={offset}.")
        map.offset_ops(offset)
        outmap.operations += map.as_ops()
    return outmap


def path_to_Shmap(inpath):
    return Shmap(inpath.name, import_map(inpath))


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
    """combines .json format shmeppy maps into one .json file"""
    print(" =================")
    print("   MAP COMBINER   ")
    print(" =================")
    print("Press ctrl+c or close window to quit.\n")
    print("Will take any number of .json map files as command line arguments:")
    print(" > combine_maps.exe <map-1 path> <map-2 path>...<map-n path>")
    print("    OR")
    print(" > python combine_maps.py <map-1 path> <map-2 path>...<map-n path>\n")

    try:
        # getting maps from command line
        if len(sys.argv) == 1:
            raise Exception("Did not find maps. Please provide below.")
        map_list = []
        for p in sys.argv[1:]:
            print(f"Provide Map Path: {p}")
            temp_p = Path.cwd().joinpath(p)
            print(f"Attempting to import map from: {temp_p.resolve()}")
            map_list.append(path_to_Shmap(temp_p))
    except Exception as e:
        # prompt for maps instead
        print(e)
        print(f"Looking for maps in: {Path.cwd().resolve()}")
        print("If maps are in this folder, just list mapname including")
        print("file extension (.json) otherwise include the folder name")
        print("E.g. mymap.json or backup_maps/mymap.json")
        mapstr1 = input("Please provide relative path to map #1: ")
        mapstr2 = input("Please provide relative path to map #2: ")
        mpath1 = Path.cwd().joinpath(mapstr1)
        mpath2 = Path.cwd().joinpath(mapstr2)

        # try importing maps
        print("Loading Mapfiles:")
        try:
            map_list = [path_to_Shmap(mpath1), path_to_Shmap(mpath2)]
        except Exception:
            # try again
            print(f"tried: {mpath1}\n{mpath2}")
            print("\n\nERROR: File not found, let's try again (or press ctrl+c to quit)\n\n")
            return main()

    pad = input(f"Minimum PADDING between maps (in squares). Or press enter for default value of {PADDING}: ")
    pad = int(pad) if pad else PADDING

    print(f"\nOutput destination currently set to:\n {Path.cwd()}")
    outdest = input("Enter to continue, or enter full path to set output destination: ")
    outdest = Path(outdest) if outdest else Path.cwd()

    # make new map
    new_map = combine_maps(map_list, padding=pad)

    # make filename
    ts = str(datetime.now())[:-7]
    ts = ts.replace(':', '').replace('-', '').replace(' ', '_')
    filename = f"combined_map_{ts}.json"

    # export and print result
    print(export_map(new_map.json_format(), outdest.joinpath(filename)))

    # pause before exiting - necessary for pyinstaller
    input("Press Enter to Exit...")


if __name__ == '__main__':
    main()
