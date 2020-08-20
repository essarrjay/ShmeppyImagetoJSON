#! usr/bin/env python3

import json
from pathlib import Path
from collections import Counter
from copy import deepcopy
import sys

PADDING = 2
BASE_PATH = Path(__file__).resolve().parent.parent
MAP_PATH = BASE_PATH.joinpath('extra_files','investigation_files','asof_beach.json')
WS_OLD = BASE_PATH.joinpath('extra_files','investigation_files','white_square.json')
WS = BASE_PATH.joinpath('extra_files','investigation_files','2X2whitesquare1op.json')
CELL_OPS = {'FillCells':['cellFills'], 'UpdateCellEdges':["top","left"]}
OTHER_OPS = {'CreateToken':['color','position']}

SHMEP_DICT = {"exportFormatVersion":1,"operations":[]}

def get_map_bounding_box(map):
    """returns bouding box of a map in squares x,y"""
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
    outmap = deepcopy(SHMEP_DICT)
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
    print(f"Successful Import of map: {inpath}")
    return map_dict

def export_map(map, outpath):
    """exports map to outpath"""

    print(f"\nExporting to {outpath}\n")
    with outpath.open(mode='w') as j_file:
        json.dump(map, j_file, indent=2)
    return f"Exporting to {outpath}"

def main():
    print(" =================")
    print("   COMBING MAPS")
    print(" =================")
    outpath = BASE_PATH.joinpath('test_json','test_outputs','combined_map.json')
    try:
        map_list = []
        for p in sys.argv[1:]:
            print(f"p = {p}")
            temp_p = BASE_PATH.joinpath(p)
            print(f"temp p = {temp_p}")
            map_list.append(import_map(temp_p))
    except Exception as e:
        print(e)
        print("If maps are in the same folder, just list mapname including file extension .json")
        mpath1 = input("Please provide relative path to map #1:")
        mpath2 = input("Please provide relative path to map #2:")
        map_list = [import_map(mpath1),import_map(mpath2)]

    new_map = combine_maps(map_list,padding=PADDING)
    export_map(new_map,outpath)

if __name__ == '__main__':
    main()

#python ./src/combine_maps.py ./test_json/2x2whitesquare1op.json ./test_json/2x2whitesquare1op.json ./test_json/2x2whitesquare1op.json
#python ./src/combine_maps.py ./test_json/2x2whitesquare1op.json ./test_json/2x2square4ops.json
#python ./src/combine_maps.py ./test_json/2x2square4ops.json ./test_json/2x2square4ops.json

#python ./src/combine_maps.py ./test_json/eandc10ops.json ./test_json/2x2square4ops.json ./test_json/eandc10ops.json

#python ./src/combine_maps.py ./test_json/asof_bea.json ./test_json/2x2square4ops.json
