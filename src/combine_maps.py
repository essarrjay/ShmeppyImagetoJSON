#! usr/bin/env python3

import json
from pathlib import Path
from collections import Counter
from copy import deepcopy
import sys
from datetime import datetime

PADDING = 10
BASE_PATH = Path(__file__).resolve().parent.parent
#SAME_PATH = Path(__file__).resolve().parent
CELL_OPS = {'FillCells':['cellFills'], 'UpdateCellEdges':["top","left"]}
OTHER_OPS = {'CreateToken':['color','position']}
SHMEP_DICT = {"exportFormatVersion":1,"operations":[]}

def get_map_bounding_box(map):
    """returns bounding box of a map in squares x,y"""
    print(f" --------------------")
    print(f" Getting Bounding Box")
    print(f" --------------------")
    x_list,y_list = [],[]

    for op in map['operations']:
        print(f"op_type is {op['type']}")
        if op['type'] in CELL_OPS.keys():
            for action in CELL_OPS[op['type']]:
                if op['type'] in ["FillCells","UpdateCellEdges"]:
                    xs,ys=fillcells_xys(op[action])
                #TODO: add other op types
                    x_list += xs
                    y_list += ys
        else:
            print(f"{op['type']} is NOT drawing op")
    ul_corner = min(x_list),min(y_list)
    lr_corner = max(x_list),max(y_list)
    return ul_corner,lr_corner

def fillcells_xys(action):

    """returns lists of x,y coords"""
    x_list = []
    y_list = []
    for cell in action:
        x,y = cell[0]
        x_list.append(x)
        y_list.append(y)
    return x_list,y_list

def get_new_corners(bb1,bb2):
    """returns tuple of corners describing box bounding two bounding boxes"""
    (ux1,uy1),(lx1,ly1) = bb1
    (ux2,uy2),(lx2,ly2) = bb2
    ul_corner = min(ux1,ux2),min(uy1,uy2)
    lr_corner = max(lx1,lx2),max(ly1,ly2)
    return ul_corner,lr_corner

def get_dimensions(bb):
    """returns absolute dimensions of bounding box"""
    (ux,uy),(lx,ly) = bb
    return lx-ux+1,ly-uy+1

def count_ops(map):
    print("................")
    print("Operations Count")
    print("................")
    op_list = []
    for op in map['operations']:
        op_list.append(op['type'])
    for k,v in Counter(op_list).most_common():
        print(f'{k} : {v}')

def translate_op(op,offset,new_id):
    """translate op by offset value"""
    for action in CELL_OPS[op['type']]:
        cell_list = []
        for cell in op[action]:
            x = cell[0][0]+offset[0]
            y = cell[0][1]+offset[1]
            cell_list.append([[x,y],cell[1]])
        op[action] = cell_list
    op["id"] = new_id
    return op

def get_updated_ops(map,offset):
    """for map, offset all draw operations"""
    outops = []
    for op in map['operations']:
        if op['type'] in CELL_OPS.keys():
            #print(f"translating {op['type']} by the following dimensions: {offset}")
            outops.append(translate_op(op,offset,new_id='1234'))
        elif op['type'] in OTHER_OPS:
            pass
    return outops

def combine_maps(map_list,layout=(0,1),padding=0):
    """combine maps in map_list with padding"""
    total_x,total_y = 0,0
    h,v = layout
    layout = {}
    for map in map_list:
        bb = get_map_bounding_box(map)
        print(f"bounding boxes = {bb}")
        md = get_dimensions(bb)
        print(f"map dimensions = {md}")

        #create relative placement of map
        x = total_x-bb[0][0]
        y = total_y-bb[0][1]

        layout.update({(x,y):(map,md)})

        #set next map's coordinates
        total_x += (md[0]+padding)*h
        total_y += (md[1]+padding)*v

    print(" +++++++++++++++++++++++++++++++")
    print("  Writing New Drawing Operations")
    print(" +++++++++++++++++++++++++++++++")

    #translate maps
    outmap = deepcopy(SHMEP_DICT)
    i = 1
    for offset,(map,md) in layout.items():
        print(f"Map #{i} of size {md[0]}x{md[1]} being offset by x,y={offset}.")
        outmap['operations'] += get_updated_ops(map,offset)
        i += 1

    return outmap

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
    except FileNotFoundError as e:
        result = f"Export failed, please enter a valid output destination."
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

    #maps from command line
    try:
        if len(sys.argv) == 1: raise Exception("Did not find maps. Please provide below.")
        map_list = []
        for p in sys.argv[1:]:
            print(f"Provide Map Path: {p}")
            temp_p = BASE_PATH.joinpath(p)
            print(f"Attempting to import map from: {temp_p}")
            map_list.append(import_map(temp_p))
    except Exception as e:
        print(e)
        print(f"Looking for maps in: {BASE_PATH.resolve()}")
        print("If maps are in this folder, just list mapname including")
        print("file extension (.json) otherwise include the folder name")
        print("E.g. mymap.json or backup_maps/mymap.json")
        mpath1 = input("Please provide relative path to map #1: ")
        mpath2 = input("Please provide relative path to map #2: ")

        #import maps
        print("Loading Mapfiles:")
        try:
            map_list = [import_map(BASE_PATH.joinpath(mpath1)), import_map(BASE_PATH.joinpath(mpath2))]
        except:
            print(f"tried: {BASE_PATH.joinpath(mpath1)}\n{BASE_PATH.joinpath(mpath2)}")
            print(f"\n\nERROR: File not found, let's try again (or press ctrl+c to quit)\n\n")
            return main()

    pad = input(f"Spacing between maps in squares (or press enter for default value of {PADDING}): ")
    pad = int(pad) if pad else PADDING

    print(f"\nOutput destination currently set to:\n {BASE_PATH}")
    outdest = input(f"Enter to continue, or enter full path to set output destination: ")
    outdest = Path(outdest) if outdest else BASE_PATH

    new_map = combine_maps(map_list,padding=pad)

    ts = str(datetime.now())[:-7]
    ts = ts.replace(':','').replace('-','').replace(' ','_')
    filename = f"combined_map_{ts}.json"

    print(export_map(new_map,outdest.joinpath(filename)))

    #pause before exiting - necessary for pyinstaller
    input("Press Enter to Exit...")

if __name__ == '__main__':
    main()
