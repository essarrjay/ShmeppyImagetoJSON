
# **Simple Shmeppy Mapfile (JSON) Generator**

For the most excellent [shmeppy.com](https://shmeppy.com/) minimalist virtual tabletop application.

Many thanks to John Sullivan for their awesome, thoughfully designed and currently free!?! product.

More info on Shmeppy here: https://shmeppy.com/about

# **Overview of Tools**
## Image Converter
**Main documentation:** `docs/image_converter.md`
The `shmeppify.py` script (in conjunction with others) takes an image  and converts it into a form recognized by Shemppy's new import function.

## Map Combiner
**Main documentation:** docs/map_combiner.md
The `combine_maps.py` script creates a single Shmeppy `.json` map file from two (or more) other Shmeppy `.json` map files. Good for combining

# Quickstart

### **Launching Application**
To use, you have two options:
#### **Python** (Windows, Mac, Linux)
  Download as a zip (or clone with Git), extract and run from a command line:  
  `python ./src/shmeppify.py <*image_file_path>`  
  * The image can also be specified later from an input prompt.
  * Will likely need to install additional packages (see detailed instructions below)  

#### Alternative to Python:
For a stand-alone application (with less functionality) see the `/build/` folder. The `.zip` and `.exe` files should work by themselves without installing Python. The `.exe` files are self-contained, whereas the `.zip` contains a `.exe` but contains multiple separate files which some users may find confusing. The `.zip` packages will run more quickly and contains bundled README files.

See `build/README.md` for more info.

### **Use**
See `/docs/` for information on using these tools.

#### Use: Image Converter Summary
Navigate to main project directory. Run the script using:  

`python ./src/shmeppify.py <*image_file_path>`  
or
`./Image_to_Shmeppy_JSON_v2.2.1.exe <*image_file_path>`

(depending on which file you have)

* The image can also be specified later from an input prompt.
* Will likely need to install additional packages (see detailed instructions below)  

After a possible prompt to provide an input file, you will see prompts to specify the processing method, and the map dimensions.

The maximum map dimension sets the scale of the Shmeppy map - typically one 5x5 ft map square = one Shmeppy tile, but some players use a different scale (e.g. one map square equal to 2x2 Shmeppy tiles).

Output map will be in the current working directory.  

Import the `.json` file into Shmeppy using the `Games >>` sidepanel in the upper left.

**Note:** This script will only generate a map using 'fill' - not any 'edges'

Navigate to main project directory. Run the converter script using:  

#### Use: Map Combiner Summary

Navigate to main project directory. Run the script using:
`python ./src/combine_maps.py <map_path_1> <map_path_2>...<map_path_n>`
or
`./map_combiner_v0.2.3.exe <*image_file_path>`

(depending on which file you have)

* The maps can also be specified later from an input prompt.
* Uses standard python packages
* Minimum spacing between maps can be specified through a prompt.

-----

# **Detailed Instructions**

## Simple start for Windows (no Python)
No need to install python, but you'll be limited to when specific builds are created.

1. In [/build](https://github.com/essarrjay/ShmeppyImagetoJSON/tree/master/build) download Image_to_Shmeppy_JSON_v2.x.x.zip
2. Extract
2. (optional) place image file in `Image_to_Shmeppy_JSON_v2.x.x` or `Image_to_Shmeppy_JSON_v2.x.x\Maps`
3. Run `Image_to_Shmeppy_JSON_v2.x.x.exe` from within Image_to_Shmeppy_JSON_v2.x.x folder.
4. Output map will be in the current working directory.

You will be prompted to supply the path of an input image, or can provide it directly from a command line:
`Image_to_Shmeppy_JSON_v2.x.x.exe <*image_file_path>`

If you're new to command line usage, you can usually type just a few letter of a filename then hit `Tab` to autocomplete.

Also, the arrow keys `↑`or`↓` will let you cycle through recent entries, which makes repeat operations (with different settings) a bit easier.

## Python: Installing and Use

Installing python will provide the most reliable use of this tool, as well as allow you to access the most recent updates to the script.

### Prerequisites: Python
You'll need a Python interpreter - this is basically a program that lets you run scripts/programs written in the programming language of Python.

#### Install Instructions:
Guide here:  https://wiki.python.org/moin/BeginnersGuide/Download  
(or plenty of other guides if you google "Installing Python for Windows/Linux/Etc")

### **Download these files**
Oh, tons of ways to do this. Click on the green `Code ▼` button toward the upper right, click "download zip". Unzip folder someplace convenient on your computer (we'll assume your desktop).

### **Download the needed libraries**
[Upgrade or install Pip](https://pip.pypa.io/en/stable/installing/#upgrading-pip) the package manager. It comes standard if you used the python install link above.

#### Install any missing packages
Python includes a strong standard library, but this program uses a few additional packages you may not have installed:  

haishoku  
cutie
Pillow (commonly included with Python interpreters)

A full list of packages and their purposes can be found at the bottom of this document.

##### To install missing packages
open a command line and run:
`python -m pip install -r requirements.txt`

##### more detailed instructions
You can see all installed packages by using the following commands in a terminal (see next section if you need help):  
`pip list` or `python -m pip list`

Install a package using:  
`pip install <package name>` or `python -m pip install <package name>`

For example:  
`python -m pip install haishoku cutie Pillow`

Package names are case sensitive.

### **Running the script**

#### Open a terminal window.

**Linux**: If you use Linux you probably know how already.

 **Windows**: `Win` + `x`, followed by `i` to open Windows PowerShell

 Having trouble? [More ways to access PowerShell](https://www.tenforums.com/tutorials/25581-open-windows-powershell-windows-10-a.html)

#### Run the script
In the terminal window, navigate to the folder where you saved both the script and your image file. For example, if you were using Windows and saved both on your desktop the command would be:    
`cd desktop\ShmeppyImagetoJSON` or   
`cd C:\users\<your_username>\desktop\ShmeppyImagetoJSON`

Call the script by entering the following command:  
`.\src\python shmeppify.py`

You will be prompted to enter the path for the image file. If it's in the `\ShmeppyImagetoJSON\` folder, just enter the file name, including the file extension. (e.g. `example_file.jpg`)

You will then see prompts to specify the processing method, and the map dimensions.

The maximum map dimension sets the scale of the Shmeppy map - typically one 5x5 ft map square = one Shmeppy tile, but some players use a different scale (e.g. one map square equal to 2x2 Shmeppy tiles).

The map file will named something like `<image_name>_<width>x<height>_2020...` and current working directory. The console should also have an line describing where the file was saved.

### Import into Shmeppy  
Navigate to Shmeppy.com, click on the `Games >>` button in the upper right. At the bottom of the side panel, click on `Import Backup` and select the file you created earlier with the script.

Import the `.json` file into Shmeppy using the `Games >>` sidepanel in the upper left.

**Note:** This script will only generate a map using 'fill' - not any 'edges'

### **Need Help?**
Don't bug John! But feel free to bug me, or jump on the discord and try asking there:
https://shmeppy.com/help-and-community

### **Other feedback is welcome!**
The last time I did serious programming was on a Commodore64 (or feels like it at least). Feel free to send a message if you're having any issues.

## **Notes:**
#### Uses packages:  
json  (for exporting the map)  
datetime (used for map file names)  
pathlib (to aid in compatibility across different operating systems)  
sys (system stuff like take command line arguments and exit the program)  
haishoku (palette related functions)  
Pillow (also known as PIL, used for general image processing)  
cutie (user input menu)  

**For reference, build using these versions of the non-standard packages:**
haishoku == 1.1.8
cutie == 0.2.2
Pillow == 7.2.0

#### Versions:
V1 basic BOX and NEAREST filter/resize processing  
V2 Palette processing and additional filters  
V2.2 Palette sampling introduced
V2.3 Map combiner included
