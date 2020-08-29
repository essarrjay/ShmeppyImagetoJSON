# Map Tools

## Combine Maps

#### Use: combinemaps.py Summary

1. Navigate to main project directory.  
2. Run the script using:
`python ./shmeppytools/maptools/combine_maps.py <map_path_1> <map_path_2>...<map_path_n>`  
or  
`./map_combiner_v0.2.3.exe <*image_file_path>`  

(depending on which file you have)

* The maps can also be specified later from an input prompt.
* Uses standard python packages
* Minimum spacing between maps can be specified through a prompt.

## Collect Tokens from map(s)

#### Use: collecttokens.py Summary

1. Navigate to main project directory.  
2. Run the script using:
`python ./shmeppytools/maptools/collecttokens.py <map_path_1> <map_path_2>...<map_path_n>`  

* The maps can also be specified later from an input prompt.
* Spacing between tokens (and tokens from separate maps) may be specified on the command line.

This script creates a new map using all tokens from the input map(s). Tokens are grouped. Takes 1 or more `.json` map files. This can be useful to move tokens from one map to another. If run from the command line, using the `-c` flag combines tokens from multiple maps into one map. Omitting will process each map separately.  Type `python simple_map_to_tokens.py -h` for more options.
