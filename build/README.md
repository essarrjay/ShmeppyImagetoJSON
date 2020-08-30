# **Builds**
## **Full Python Bundles**
`shmeppytools_python_bundle_vx.x.x.tar` is a great way to grab all the needed python files including the README and docs files as `.html`.

##### Pros:
* Good if you're new to running source code and don't feel comfortable cloning or downloading the whole repo.
* Works on Linux, Mac or Windows
* More current than the `.exe` builds, more features and ~~fewer~~*different* bugs.

##### Cons:
* Will require installing python (see main README), and packages. Not very challenging, but does take a few minutes.

## **Executables ("programs/applications")**
These are organized by function, as they haven't been updated since the Image Converter and Map Tools features have been combined.

## Image Converters
#### Image_to_Shmeppy_JSON_v2.2.1.zip
A stand-alone Windows application which does not require installing python.

##### Pros:
* Does not require installing python or packages

##### Cons:
* Windows only
* Dated - only contains the `imageconverter` functions (images to Shmeppy maps) and does not contain any map tools (merging maps, fetching tokens).
* May have more bugs than the python scripts

##### simple_shmeppify_v1.1.0.exe
An even simpler single-file stand-alone Windows application. Download and run.
##### Pros:
* Does not require installing python or packages
* A single file, no need to extract ahead of time.

##### Cons:
* slower to start up than the `.zip` package
* same issues as `Image_to_Shmeppy_JSON_v2.2.1.zip`

## Map Tools
#### map_combiner_v0.2.3.exe
Combines 2 or more `.json` map files into a single map file suitable for import into Shmeppy.
##### Pros:
* It's a single file application. Save file to directory containing map exports, double click to run, you'll be prompted for maps. Also takes maps paths from the command line.
##### Cons:
* Windows only
* Dated, only combines maps one below the other.
* Due to the structure of the "complier" you may have to provide input maps using a prefix of `./` e.g. `./mymap.json` or `./myfolder/mymap.json`

#### token_getter_v0.1.1.exe
Fetches tokens from a map, groups tokens and outputs as a new map. Great if you don't want to have to recreate player tokens, initiative trackers (along with their associated palette).
##### Pros:
* It's a single file application. Save file to directory containing map exports, double click to run, you'll be prompted for maps. Also takes maps paths from the command line.
##### Cons:
* Windows only
* Dated, only combines maps one below the other.
* Due to the structure of the "complier" you may have to provide input maps using a prefix of `./` e.g. `./mymap.json` or `./myfolder/mymap.json`
