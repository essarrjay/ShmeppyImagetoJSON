
# **Simple Shmeppy Mapfile (JSON) Generator**

For the most excellent [shmeppy.com](https://shmeppy.com/) minimalist virtual tabletop application.

Many thanks to John Sullivan for their awesome, thoughfully designed and currently free!?! product.

More info on Shmeppy here: https://shmeppy.com/about

# **Overview**
This script takes an image (`.jpeg`, `.png` or probably plenty others) and converts it into a form recognized by Shemppy's new import function.

To use, call from a command line:  
`python shmeppify.py <*image_file_path>`

The image can also be specified later from an input prompt.

You will then see prompts to specify the processing method, and the map dimensions.

The maximum map dimension sets the scale of the Shmeppy map - typically one 5x5 ft map square = one Shmeppy tile, but some players use a different scale (e.g. one map square equal to 2x2 Shmeppy tiles).

Import the `.json` file into Shmeppy using the `Games >>` sidepanel in the upper left.

**Note:** This script will only generate a map using 'fill' - not any 'edges'

## ► Processing Options ◄

### **PALETTE**
Attempts to convert image to Shmeppy fill tiles, using a palette of colors.
- Sharp color transitions when processing an image with fixed color palette.
- Many similar colors in a single image may return a poor result.

#### **Palette Sampling**
The palette is generated (slowly, improved method in progress) by slicing the map image into smaller images, then fetching the most commonly used colors in those images.

The sample grid is autoscaled from the image's largest dimension using the provided sample maximum map dimension. For example, using a sample grid maximum map dimension of 4 on an image of 1600x1200px would result in a sample grid of 4x3 tiles, each 400x300px.

The most used colors of each sample tile (exact number specified by user as palette size) is added to the overall palette for the final map.

Obviously, the options for **palette sampling** can drastically affect the map processing speed, but provides the more control than the **filter-resize** method.

-----
### **FILTER RESIZE**
Scales the image to the map size then converts pixels to Shmeppy tiles.  

- Much faster than Palette
- Color gradient. Good for landscapes with similar gradients, e.g. beaches, grass fields

Both methods preserve the aspect ratio of the map.

#### **Filter Types**

(from https://pillow.readthedocs.io/en/stable/handbook/concepts.html#filters)

Listed in order increasing order of fidelity, decreasing order of speed.

**NEAREST** - Pick one nearest pixel from the input image.
    Ignore all other input pixels.

**BOX** - Each pixel of source image contributes to one pixel of
    the destination image with identical weights

**BILINEAR** - Calculate the output pixel value using linear
    interpolation on all pixels that may contribute to the output
    value.

**HAMMING** - Produces a sharper image than BILINEAR, doesn’t have
    dislocations on local level like with BOX.

**BICUBIC** - Calculate the output pixel value using cubic
    interpolation on all pixels that may contribute to the output
    value.

**LANCZOS** - Calculate the output pixel value using a high-quality
    Lanczos filter (a truncated sinc) on all pixels that may
    contribute to the output value.

## **Detailed Instructions on Getting Started:**

### Prerequisites: Python
You'll need a Python interpreter - this is basically a program that lets you run scripts/programs written in the programming language of Python.

#### Install Instructions:
Guide here:  https://wiki.python.org/moin/BeginnersGuide/Download  
(or plenty of other guides if you google "Installing Python for Windows/Linux/Etc")

### **Download these files**
Oh, tons of ways to do this. Click on the green `Code ▼` button toward the upper right, click "download zip". Unzip folder someplace convenient on your computer (we'll assume your desktop).

### **Download the needed libraries**
[Upgrade or install Pip](https://pip.pypa.io/en/stable/installing/#upgrading-pip)

#### Install any missing packages
Python includes a strong standard libary, but this program uses a few additional packages you may not have installed:  

haishoku  
Pillow  
cutie

A full list of packages and their purposes can be found at the bottom of this document.

You can see all installed packages by using the following commands in a terminal (see next section if you need help):  
`pip list` or `python -m pip list`

Install a package using:  
`pip install <package name>` or `python -m pip install <package name>`

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
`python shmeppify.py`

You will be prompted to enter the path for the image file. If it's in the same folder as the script, just enter the file name, including the file extension. (e.g. `example_file.jpg`)

You will then see prompts to specify the processing method, and the length of the longest map edge.

The maximum map dimension sets the scale of the Shmeppy map - typically one 5x5 ft map square = one Shmeppy tile, but some players use a different scale (e.g. one map square equal to 2x2 Shmeppy tiles).

The map file  you file will named something like `game_map_2020...` and located in the `./ShmeppyImagetoJSON/output_files/` folder. Rename if you like.

### Import into Shmeppy  
Navigate to Shmeppy.com, click on the `Games >>` button in the upper right. At the bottom of the side panel, click on `Import Backup` and select the file you created earlier with the script.

Import the `.json` file into Shmeppy using the `Games >>` sidepanel in the upper left.

**Note:** This script will only generate a map using 'fill' - not any 'edges'

### **Need Help?**
Don't bug John! But jump on the discord and try asking there:
https://shmeppy.com/help-and-community

### **Other feedback is welcome!**
The last time I did serious programming was on a Commodore64 (or feels like it at least). I sure hope it works!

## **Notes:**
#### Uses packages:  
json  (for exporting the map)  
datetime (used for map file names)  
pathlib (to aid in compatibility across different operating systems)  
sys (system stuff like take command line arguments and exit the program)  
haishoku (palette related functions)  
Pillow (also known as PIL, used for general image processing)  
cutie (user input menu)  

#### Versions:
V1 basic BOX and NEAREST filter/resize processing  
V2 Palette processing and additional filters
