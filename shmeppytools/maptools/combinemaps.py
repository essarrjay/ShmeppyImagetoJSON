#! usr/bin/env python3
"""combinemaps.py

Merges 2 or more maps into a single .json shmeppy map file.
"""

# external modules
import json
from pathlib import Path
import argparse
from math import ceil

# internal modules
from shmap import Shmap
import uihelper

PADDING = 10
SHORTCUT_DICT = {'v':'vertical', 'h':'horizontal', 'g':'gridv', 'gv':'gridv', 'gh':'gridh'}

def combine_maps(shmaps_list, max_col=1, padding=0):
    """combine maps in map_list with padding"""
    total_x, total_y = 0, 0
    layout = {}
    col, row = 1, 1
    max_row = ceil(len(shmaps_list)/max_col)
    map_heights = {i: [] for i in range(1, max_row+1)}
    map_widths = {i: [] for i in range(1, max_col+1)}
    print(f"Maps to be arranged in a grid of {max_col}x{max_row}.")

    for map in shmaps_list:
        bb = map.set_bounding_box()
        print(f"Map: {map.name}")
        print(f"bounding box = {bb}")
        mapdim = map.get_bb_dimensions()
        print(f"map dimensions = {mapdim}")

        # store layout info
        layout.update({(col, row): (map, bb, mapdim)})
        print(f"map grid address = {col},{row}")

        # collect widths/heights to set grid size
        mw, mh = mapdim
        map_heights[row].append(mh)
        map_widths[col].append(mw)

        # set next map's grid coordinates
        if col != max_col:
            col += 1
        else:
            col = 1
            row += 1

    print(" +++++++++++++++++++++++++++++")
    print("  Writing New Draw Operations")
    print(" +++++++++++++++++++++++++++++")

    # calculate grid sizes
    gridpos = {}
    for row, heights in map_heights.items():
        height = max(heights)
        for col, widths in map_widths.items():
            width = max(widths)
            gridpos.update({(col, row): (total_x, total_y)})
            total_x += width+padding
        total_x = 0
        total_y += height+padding

    # offset and merge maps
    outmap = Shmap('combined_map')
    for gridsquare, (map, bb, mapdim) in layout.items():
        offset = list(gridpos[gridsquare])
        offset[0] -= bb[0][0]
        offset[1] -= bb[0][1]
        print(f"\nMap {map.name} of size {mapdim[0]}x{mapdim[1]}, occupying girdsquare {gridsquare} being offset by x,y={offset}.")
        map.offset_ops(offset)
        outmap.operations += map.as_ops()
    return outmap


def get_maps_per_row(arrange, map_quant):
    """returns # of columns given arrangement and # of maps"""
    max_col_dict = {'vertical':1, 'horizontal':map_quant, 'gridv':round(map_quant**0.5), 'gridh':ceil(map_quant**0.5)}
    if arrange not in max_col_dict.keys():
        arrange = SHORTCUT_DICT[arrange]
    print(f"max cols = {max_col_dict[arrange]}")
    return max_col_dict[arrange]


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

    # parser init and parse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("maps", metavar="<map path>", help="Combine each map's tokens into a single output file.", nargs='*')
    parser.add_argument("-sc", "--skipconfirm", help="Skip confirmation prompt for output destination", action="store_true", default=False)
    parser.add_argument("-p", "--padding", type=int, default=PADDING, metavar="<integer>", help="Padding between maps")
    parser.add_argument("-a", "--arrange", help="Arrange maps vertically, horitzontally or in a grid pattern.", choices=['vertical', 'horizontal', 'gridv', 'gridh']+list(SHORTCUT_DICT.keys()), default='vertical')
    parser.add_argument("-d", "--destination", metavar="<path>", help="Output destination path for .json file.")
    parser.add_argument("-nep", "--noexitpause", help='Skip "Press Enter to Exit..."', action="store_true")
    args = parser.parse_args()
    print(f'Command Line Arguments, as parsed:\n   {vars(args)}\n')

    # get maps from command line
    shmaps_list = uihelper.get_shmaps(args.maps, min_num=2)

    # check for padding
    if args.padding or args.padding == 0:
        pad = args.padding
    else:
        pad = input(f"Minimum PADDING between maps (in squares). Or press enter for default value of {PADDING}: ")
        pad = int(pad) if pad else PADDING

    # prompt output destination or skip confirmation
    if args.skipconfirm:
        outdest = Path(args.destination) if args.destination else Path.cwd()
    else:
        print(f"\nOutput destination currently set to:\n {Path.cwd()}")
        outdest = input("Enter to continue, or enter full path to set output destination: ")
        outdest = Path(outdest) if outdest else Path.cwd()

    # layout and make new map
    maps_per_row = get_maps_per_row(args.arrange,len(shmaps_list))
    new_map = combine_maps(shmaps_list, maps_per_row, padding=pad)

    # export and print result
    print(new_map.export_to(outdest))

    if not args.noexitpause:
        # pause before exiting - necessary for pyinstaller
        input("Press Enter to Exit...")


if __name__ == '__main__':
    main()
