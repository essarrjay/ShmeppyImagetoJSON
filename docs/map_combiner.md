# **Map Combiner**

# Use Overview

Navigate to main project directory. Run the converter script using:

`python ./src/combine_maps.py <map_path_1> <map_path_2>...<map_path_n>`  

* Will take as many `.json` map files as you provide from the command line.
* If no files provided or it encounters trouble loading any maps, you will be prompted to provide 2 maps.
* Fills and Edges are moved, but not tokens or fog of war.
* Application determines the outer most coordinates of the fill and edge elements of the map. It can be thought of a the smallest bounding box incorporating all fill and edge elements of the map - but not tokens.
* Maps are combined one below the other, padded between (invisible) bounding boxes.
* You can specify vertical padding between maps, or leave blank to default to 10 squares.
* Previous deletions of fills or edges may cause excessive spacing. (i.e. at the moment the program cannot determine if a previously filled in cell is still filled)
