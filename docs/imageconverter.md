# **Image Converter**

The image converter has two main methods:

### FILTER-RESIZE
Scales the image down to the map size such that 1 pixel = 1 Shemppy square, then converts pixels to Shmeppy squares.  

- Much faster than Palette
- Color gradient. Good for landscapes with similar gradients, e.g. beaches, grass fields
- Hard edges and lines in the source image will usually be blurry on the output map.

### PALETTE SAMPLING
Generates a palette of colors from the source image, then assigns a color to a Shmeppy map square based on the most commonly used color in a corresponding area of the source image. See below for details.
- Creates sharp color transitions when processing an image with large areas of uniform color and a fixed palette.
- Many similar colors but not identical colors in a single image may return a poor result.
- Terribly inefficient (dozens of seconds rather than seconds), but still a very effective timesaver when converting images to Shmeppy maps.

# Use Overview

Navigate to main project directory. Run the converter script using:

`python ./shmeppytools <*image_file_path>`  

After a possible prompt to provide an input file, you will see prompts to specify the processing method, and the map dimensions.

The maximum map dimension sets the scale of the Shmeppy map - typically one 5x5 ft map square = one Shmeppy tile, but some players use a different scale (e.g. one map square equal to 2x2 Shmeppy tiles).

Output map will be in the current working directory.  

Import the `.json` file into Shmeppy using the `Games >>` sidepanel in the upper left.

**Note:** This script will only generate a map using 'fill' - not any 'edges'

# General Menu Options

### Menu Option: *Autoscale*  
**Default Value:** *YES*  
If yes, provide the number of squares to use for the longest (major) map dimension (horizontal or vertical) - the other dimension will be automatically calculated.  

If no, you will need to provide both the horizontal (x) and vertical (y) dimensions for the image - Can be useful for distorting or correcting the image.   

### Menu Option: *Debug Mode*  
**Default Value:** *NO*  
If yes, provides more detailed (and possibly overwhelming) info during processing.

## Menu Option: *Proceed with Processing*  
**Default Value:** *YES*  
Last chance to cancel before spending time processing. Select *NO* if you would like to start over.

----

# Method Specific Menu Options

See the appropriate processing option for details on the menu options you are presented.

## **FILTER RESIZE**
Scales the image down to the map size such that 1 pixel = 1 Shemppy square, then converts pixels to Shmeppy squares.  

- Much faster than Palette
- Color gradient. Good for landscapes with similar gradients, e.g. beaches, grass fields

### Menu Option: *Filter Types*

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

-----

## **PALETTE**
Attempts to convert image to Shmeppy fill tiles, using a palette of colors.
- Sharp color transitions when processing an image with fixed color palette.
- Many similar colors in a single image may return a poor result.
- Terribly inefficient (dozens of seconds rather than seconds), but still a very effective timesaver when converting images to Shmeppy maps.

###  Menu Option: *Sample Grid*  
The palette is generated  by slicing the map image into smaller images, then fetching the most commonly used colors in those images.

The sample grid is autoscaled from the image's largest dimension using the provided sample factor. For example, using a sample factor of 4 on a 1600x1200px image of would result in a 4x3 sample grid of  400x300px tiles.

Setting the sample factor to 1 generates an overall palette of up to 8 colors (set at the next prompt) from the whole image.

###  Menu Option: *Palette Colors*  
The app selects the top [this number] of colors from each sample tile to be used in the overall palette of the final map output.

Selecting `0` will only choose colors which occur more than 12.5% of the time on the sample tile. Works better with a larger sample grid (smaller sample tiles).

### Menu Option: **Rescale before Palette**

To speed up operation, you may rescale an image prior to processing through palette operations. This is identical to resizing an image to a lower resolution, then passing that image to this script.

The image will be resized such that each square of the final Shmeppy map is generated from a 16x16px area of the resized image. The Shmeppy map size (in squares) is still set by the user and the image aspect ratio (if autoscaled).

### **Map Generation**

The script then generates a Shmeppy map using a similar method as when determining the overall palette. The image is sliced into smaller images, with each image representing a single square or tile of the completed Shmeppy map.

For example, an image of 800x600px converted to a map of 80x60 squares would use tiles of 10x10 pixels.

The Shmeppy square is colored using the previously generated palette - the palette color nearest the dominant color of the image slice/tile becomes the square color.

Obviously, the options for **palette sampling** can drastically affect the map processing speed, but provides the more control than the **filter-resize** method.

This is not very efficient process, and will probably be improved upon (or re-implemented) in the future. But it currently works, and still only takes 30 seconds or so. It works really well with images using a limited palette already, rather than many gradients.
