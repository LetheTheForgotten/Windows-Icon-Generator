# Windows Icon Generator
Python based cli script that uses pillow or gimp to take the first image of every folder in a given directory, convert it to an icon and assign it to the folder its in by editing Desktop.ini

# prerequisites:
python:

https://www.python.org/


pillow: 

https://pillow.readthedocs.io/en/stable/index.html

optionally:

gimp: 

https://www.gimp.org/downloads/

# Useage:
`python converter.py INPUT`

Script will then generate an .ico file of the first image in the folder and edit the Desktop.ini file to assign it as the icon of the folder.

Iterates into each subfolder.

If no images are found, leaves folder untouched

# Arguments:
|Argument        |Description|
| --------------- |----------|
|INPUT| input filepath to have icons generated for. Required.|
|--gimp `path` |Filepath to locally installed gimp command line executable(gimp-console.exe). Using this will make the program use the GIMP CLI rather than pillow to convert images into icons. Results in Higher Quality but is more intensive |
|--timeout `timeout` |Override for gimp image processing timeout, in seconds. Default is 10 seconds. -1 disables timeout, requiring manual closure of the gimp cli window |
|--iconsonly|creates .ico files without assigning them|
|--iconoverwrite|skips the prompt when overwriting an existing .ico file with a default y/n answer. 1 will always overwrite the existing file, 0 will always skip it|
|--uselast|Makes Icon generation use the last image in a folder rather than the first one.|
|--reg|Uses first/last image matching given regex as icon.|
|--v|verbose output.|
# Troubleshooting

## small icon sizes

The icons generated using pillow occasionally glitch and don't scale the icons properly with size, if this happens rerun the script or use the provided gimp alternative

## Icons not appearing

Desktop.ini only works when the folder is set to read-only, run `attrib +r * /d` on the command line in the directory where icons are broken to set this.

Windows hates consistency when it comes to icons, the best option to make sure they show up is a system restart.

If you don't feel like doing that what I've found works consistently is opening and closing the customization tab of a single folder in the directory and then rerunning the script, this will usually cause all of the folders to automatically refresh.

Alternatively opening the customization tab of a folders properties and clicking ok will always cause the icon to update properly. 

Or just waiting I've had the folder icons pop in after a while doing something else. I assume this is some kind of caching thing on windows end.


