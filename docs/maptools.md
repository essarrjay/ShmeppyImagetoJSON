# **Map Tools**
These tools work with `.json` Shmeppy map files, either from exporting Shmeppy map, or from converting an image to a `.json` file using the shmeppytools imageconverter module.

Two tools (as of 2.4):
* **Merge Maps** - combine two or more .json files (includes fills, edges, tokens)
* **Fetch Tokens** - get all tokens from a map, and group together (excludes the edges/fills) 

## Combine Maps
Combines 2 or more `.json` files into one map.

#### combinemaps.py Use Overview

Navigate to main project directory. Run the converter script using:

`python ./shmeppytools`  
or  
`python ./shmeppytools/maptools/combine_maps.py <map_path_1> <map_path_2>...<map_path_n>`  

* Will take as many `.json` map files as you provide from the command line.
* If no files provided or it encounters trouble loading any maps, you will be prompted to provide 2 maps.
* Fills, Edges and Tokens are transferred to the new merged map, but not fog of war.
* Application determines the outer most coordinates of the fill and edge elements of the map. It can be thought of a the smallest bounding box incorporating all fill and edge elements of the map - but not tokens.
* Maps are combined one below the other by default, padded between (invisible) bounding boxes. May specify another arrangement using the command line argument `-a` (see below)
* You can specify padding between maps, or leave blank to default to 10 squares. May also be provided from the command line with `-p` (see below)
* Previous deletions of fills or edges may cause excessive spacing. (i.e. at the moment the program cannot determine if a previously filled in cell is still filled)

#### Command Line Arguments
Use:  
`python shmeppytools [-h] [-sc] [-p <integer>] [-a <type>] [-d <path>] [-nep] [<map path> [<map path> ...]]`

**Positional Arguments :**  
  `<map path> `(optional)  
  If not provided at the command line will be prompted for two different maps. Combine each map's tokens into a single output file.

**Other Optional Arguments:**  
  `-h`, `--help`  
  Show this help message and exit

  `-sc`, `--skipconfirm`  
  Skip confirmation prompt for output destination  

  `-p <integer>`, `--padding <integer>`  
  Padding between maps  

  `-a <type>`, `--arrange <type>`
  Arrange maps vertically, horitzontally or in a grid pattern. Default grid (`g`) biases vertically (`gridv`), can override with `gridh` or `gh`.  
  Type Options: `vertical`, `horizontal`, `gridv`, `gridh`    
  Type Shortcuts: `v`, `h`, `g`, `gv`, `gh`  

  `-d <path>`, `--destination <path>`  
  Output destination path for .json file.  

  `-nep`, `--noexitpause`  
  Skip "Press Enter to Exit..."  

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
#### Command Line Arguments
Use:
`shmeppytools [-h] [-c] [-sc] [-p <integer>] [-mp <integer>] [-fu] [-a {top,bottom,left,right}] [-d <path>] [-nep] [<map path> [<map path> ...]]`

**Positional Arguments :**  
  `<map path> `(optional)  
  If not provided at the command line will be prompted for two different maps. Combine each map's tokens into a single output file.

**Other Optional Arguments:**  
  `-h`, `--help`  
  Show this help message and exit

  `-c`, `--combine`  
  Combine each map's tokens into a single output file.

  `-sc`, `--skipconfirm`  
  Skip confirmation prompt for output destination

  `-p <integer>`, `--padding <integer>`
  Padding between tokens

  `-mp <integer>`, `--mappadding <integer>`  
  Padding between tokens grouped from separate maps

  `-fu`, `--fillunder`  Place a colored (filled) cell under each token

  `-a <type>`, `--align <type>`  
  Align along which edge of the tokens (when handling tokens larger than 1x1). Aligning tokens along their top or bottom edges will place all tokens in a horizontal line. Aligning along left or right edges will place all tokens in a  vertical line. Type options: `top`, `bottom`, `left`, `right`  

  `-d <path>`, `--destination <path>`  
  Output destination path for .json file.

  `-nep`, `--noexitpause`  
  Skip "Press Enter to Exit..."

#### Option: *padding*  
**Default Value:** *0*  
The amount of squares between individual tokens after being relocated/grouped.

#### Option: *mappadding*  
**Default Value:** *3*  
The amount of squares between tokens grouped from different maps.
