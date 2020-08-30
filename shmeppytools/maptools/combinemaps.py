#! usr/bin/env python3
"""combinemaps.py

Merges 2 or more maps into a single .json shmeppy map file.
"""

# external modules
import json
from pathlib import Path
import argparse

# internal modules
from shmap import Shmap
import uihelper

PADDING = 10


def combine_maps(shmaps_list, layout=(0, 1), padding=0):
    """combine maps in map_list with padding"""
    total_x, total_y = 0, 0
    h, v = layout
    layout = {}
    for map in shmaps_list:
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
    outmap = Shmap('combined_map')
    for offset, (map, mapdim) in layout.items():
        print(f"\nMap {map.name} of size {mapdim[0]}x{mapdim[1]} being offset by x,y={offset}.")
        map.offset_ops(offset)
        outmap.operations += map.as_ops()
    return outmap


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

    # add arguments to parser
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("maps", metavar="<map path>", help="Combine each map's tokens into a single output file.", nargs='*')
    parser.add_argument("-sc", "--skipconfirm", help="Skip confirmation prompt for output destination", action="store_true", default=False)
    parser.add_argument("-p", "--padding", type=int, default=PADDING, metavar="<integer>", help="Padding between maps")
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

    # make new map
    new_map = combine_maps(shmaps_list, padding=pad)

    # export and print result
    print(new_map.export_to(outdest))

    if not args.noexitpause:
        # pause before exiting - necessary for pyinstaller
        input("Press Enter to Exit...")


if __name__ == '__main__':
    main()
