# **Map Tools**

## Combine Maps
Combines 2 or more `.json` files into one map.

#### combinemaps.py Use Overview

Navigate to main project directory. Run the converter script using:

`python ./src/combine_maps.py <map_path_1> <map_path_2>...<map_path_n>`  

* Will take as many `.json` map files as you provide from the command line.
* If no files provided or it encounters trouble loading any maps, you will be prompted to provide 2 maps.
* Fills and Edges are moved, but not tokens or fog of war.
* Application determines the outer most coordinates of the fill and edge elements of the map. It can be thought of a the smallest bounding box incorporating all fill and edge elements of the map - but not tokens.
* Maps are combined one below the other, padded between (invisible) bounding boxes.
* You can specify vertical padding between maps, or leave blank to default to 10 squares.
* Previous deletions of fills or edges may cause excessive spacing. (i.e. at the moment the program cannot determine if a previously filled in cell is still filled)

#### Menu Option: *Padding*  
**Default Value:** *10*  
The minimum amount of squares between maps.


## Collect Tokens from map(s)
This script creates a new map using all tokens from the input map(s). Tokens are grouped. Can process maps separately, or combine all tokens into one map.

#### Use: collecttokens.py Summary

1. Navigate to main project directory.  
2. Run the script using:
`python ./shmeppytools/maptools/collecttokens.py <map_path_1> <map_path_2>...<map_path_n>`  

* The maps can also be specified later from an input prompt.
* Spacing between tokens (and tokens from separate maps) may be specified on the command line.
* Takes 1 or more `.json` map files.
* If run from the command line, using the `-c` flag combines tokens from multiple maps into one map. Omitting will process each map separately.
* Use `python simple_map_to_tokens.py -h` for more options.

This script creates a new map using all tokens from the input map(s). Tokens are grouped.

#### Option: *padding*  
**Default Value:** *0*  
The amount of squares between individual tokens after being relocated/grouped.

#### Option: *mappadding*  
**Default Value:** *3*  
The amount of squares between tokens grouped from different maps.
