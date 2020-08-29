import json
from pathlib import Path
import sys

from shmap import Shmap


def import_map(inpath):
    """import json, returns map as dict_obj"""
    with open(inpath) as j_file:
        map_dict = json.load(j_file)
    print(f"Successful Import of Map: {inpath}")
    return map_dict


def path_to_Shmap(inpath):
    """returns a shmap.Shmap obj from pathlib.Path"""
    return Shmap(inpath.stem, import_map(inpath))


def get_shmaps(maps_list, min_num=1):
    """returns a dict of {map_name: imported_json}"""
    shmap_list = []
    try:
        if not maps_list:
            raise Exception("Did not find maps. Please provide below.")
        for m in maps_list:
            print(f"Provided Map Path: {m}")
            temp_p = Path.cwd().joinpath(m)
            print(f"Attempting to import map from: {temp_p.resolve()}")
            shmap_list.append(path_to_Shmap(temp_p))

    # prompt for map if missing from args
    except Exception as e:
        print(e)
        print(f"Looking for maps in: {Path.cwd()}")
        print("If map is in this folder, just list mapname including")
        print("file extension (.json) otherwise include the folder name")
        print("E.g. mymap.json or backup_maps/mymap.json")
        maps_list = []
        for num in range(1, min_num+1):
            maps_list.append(input(f"Please provide relative path to map #{num}: "))

        # try importing maps
        print("Loading Mapfiles:")
        try:
            for m in maps_list:
                temp_p = Path.cwd().joinpath(mp)
                shmap_list.append(path_to_Shmap(temp_p))
        except Exception:
            # try again
            tstring = '\n'.join(map_paths)
            print(f"tried: {tstring}")
            print("\n\nERROR: File(s) not found, exiting program)\n\n")
            sys.exit(0)
    return shmap_list
