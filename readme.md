
# **Simple Shmeppy Mapfile (JSON) Generator**

For the most excellent [shmeppy.com](https://shmeppy.com/) minimalist virtual tabletop application.

Many thanks to John Sullivan for their awesome, thoughfully designed and currently free!?! product.

More info on Shmeppy here: https://shmeppy.com/about

## **Overview**
This script takes an image (`.jpeg`, `.png` or probably plenty others) and converts it into a form recognized by Shemppy's new import function.

To use, call from a command line:
`python shmeppify.py <*image_file_path>`

The image can also be specified later from an input prompt.

You will then see two prompts to specify the map size. The result will look nicest if you use the same aspect ratio as the original image.

Import the `.json` file into Shmeppy using the `Games >>` sidepanel in the upper left.

**Note:** This script will only generate a map using 'fill' - not any 'edges'

## **Detailed Instructions:**

### Prerequisites: Python
You'll need a Python interpreter - this is basically a program that lets you run scripts/programs written in the programming language of Python.

###### Install Instructions:
Guide here:  https://wiki.python.org/moin/BeginnersGuide/Download  
(or plenty of other guides if you google "Installing Python for Windows/Linux/Etc")

### **Download this file**
Oh, tons of ways to do this. Click on the `shmeppify.py` link in the list above. Then click on the `Raw` button on the right side of the screen.

Save this page in the same folder you have your map image, and name it `shmeppify.py`.

### **Running the script**

#### Open a terminal window.

**Linux**:  
If you use Linux you probably know how already.

 **Windows**:
 `Win` + `x`, followed by `i` to open Windows PowerShell

 Having trouble? [More ways to access PowerShell](https://www.tenforums.com/tutorials/25581-open-windows-powershell-windows-10-a.html)

#### Run the script
In the terminal window, navigate to the folder where you saved both the script and your image file. For example, if you were using Windows and saved both on your desktop the command would be:   
`cd desktop` or `cd C:\users\<your_username>\desktop`

Call the script by entering the following command:
`python shmeppify.py`

You will be prompted to enter the path for the image file. If it's in the same location as the script, just enter the file name, including the file extension. (e.g. `example_file.jpg`)

You will then see two prompts to specify the map size. The result will look nicest if you use the same aspect ratio as the original image.

The file will named something like `Game_Map_2020...` Rename if you like.

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
#### Uses libraries/modules:  
json  
datetime  
pathlib  
Pillow (PIL)  
sys  
