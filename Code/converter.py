import argparse
import os
import re
import subprocess
from PIL import Image
import sys
import ctypes

def convert_first_image(directory):
    # Checks if icon already present
    if("icon.ico" in os.listdir(directory)):
            if(args.iconoverwrite == None):

                userinput=""
                while(userinput != "Y" and userinput != "y" and userinput != "n" and userinput != "N"):
                    userinput=input("icon.ico file already present, do you want to overwrite it?[y/n]")

                if userinput=="n" or userinput=="N":
                    return
            elif args.iconoverwrite==0:
                return

    # Actual ico file generation                
    for item in os.listdir(directory):
        currentimage = os.path.join(directory, item)
        if os.path.isfile(currentimage) and (currentimage.endswith('.jpg') or currentimage.endswith('.png')or currentimage.endswith('.jpeg')):

            # gimp implementation
            if args.gimp:

                gimppath=args.gimp 
                gimppath=re.sub(r"\"",r"\\\"", gimppath)

                timeout = 10

                if args.timeout:
                    timeout=args.timeout

                    if args.timeout<0:
                        subprocess.run([gimppath,
                                        "-i",
                                        "-b",
                                        ("(let* ( (image (car (gimp-file-load RUN-NONINTERACTIVE \"" +
                                                               re.sub(r"\\",r'\\\\',currentimage) +
                                                               "\" \"" +
                                                               re.sub(r"\\",r'\\\\',currentimage) +
                                                               "\"))) (drawable (car (gimp-image-get-active-layer image))))(gimp-file-save RUN-NONINTERACTIVE image drawable \"" +
                                                               re.sub(r"\\",r"\\\\",directory+'\\icon.ico') +
                                                               "\" \""+re.sub(r"\\",r'\\\\',directory +
                                                                              '\\icon.ico') +
                                                               "\")(gimp-image-delete image))"),
                                        "-b",
                                        "(gimp-quit 0)",
                                        "-f",
                                        "-d",
                                        "-s"])
                        break
                try:   
                    subprocess.run([gimppath,
                                    "-i",
                                    "-b",
                                    ("(let* ( (image (car (gimp-file-load RUN-NONINTERACTIVE \"" +
                                                           re.sub(r"\\",r'\\\\',currentimage) +
                                                           "\" \"" +
                                                           re.sub(r"\\",r'\\\\',currentimage) +
                                                           "\"))) (drawable (car (gimp-image-get-active-layer image))))(gimp-file-save RUN-NONINTERACTIVE image drawable \"" +
                                                           re.sub(r"\\",r"\\\\",directory+'\\icon.ico') +
                                                           "\" \"" +
                                                           re.sub(r"\\",r'\\\\',directory +
                                                                  '\\icon.ico') +
                                                           "\")(gimp-image-delete image))"),
                                    "-b",
                                    "(gimp-quit 0)",
                                    "-f",
                                    "-d",
                                    "-s"],
                                   timeout=timeout )

                # if gimp won't close the cli on its own, kill it
                # (it never closes on its own god knows why)

                except Exception:
                    print(currentimage+" converted")
            else:

                # pillow implementation
                
                img= Image.open(currentimage)
                x,y = img.size
                size=max(255,x,y)
                new_img = Image.new('RGBA', (size,size), (0,0,0,0))
                new_img.paste(img,(int((size - x) / 2), int((size - y) / 2)))
                new_img.save(directory+'\\icon.ico', sizes=[(255,255)])

            break 
    return

def assign_icon(directory):
    desktopIniPath=directory+"\Desktop.ini"
    
    if (not('icon.ico' in os.listdir(directory))):
        
        print("icon.ico file not present in "+ directory)
        return

    # Set data string
    data =""
    # Check if desktop.ini already exists
    if os.path.exists(desktopIniPath):
        desktop = open(desktopIniPath,"r")
        data = desktop.read()
        desktop.close()
        os.remove(desktopIniPath)
        if("IconResource" in data):
            data=re.sub(r"IconResource=.*\n", r"IconResource=icon.ico, 0\n",data)
        else:
            data+=("\n[.ShellClassInfo]\n"+
            "IconResource=icon.ico, 0")
    else:
        data=("[.ShellClassInfo]\n"+
              "IconResource=icon.ico, 0\n"+
              "[ViewState]\n"+
              "Mode=\n"
              "Vid=\n"
              "FolderType=Pictures")
    desktop = open(desktopIniPath,"w")
    desktop.write(data)
    desktop.close()

    
    check = ctypes.windll.kernel32.SetFileAttributesW(desktopIniPath,0x02)
    if(not check):
        print(directory + " not set hidden")
    
##--- Startup ---##
parser = argparse.ArgumentParser(description="takes first image in folder, converts to .ico and assigns as folder icon")

parser.add_argument("input",
                    help="input filepath to have icons generated for",
                    type=str)

parser.add_argument("--gimp",
                    help=("Filepath to locally installed gimp executable." +
                          "Using this makes program use GIMP rather than pillow to convert images into ico." +
                          "Higher Quality but more intensive"))

parser.add_argument("--timeout",
                    help=("Override for gimp image processing timeout, in seconds. Default is 10." +
                          "-1 disables timeout, requiring manual closure of the gimp cli window"), type=int)

parser.add_argument("--iconsonly",
                    help="creates .ico files without assigning them",
                    action="store_true")

parser.add_argument("--iconoverwrite",
                    help=("overrides y/n prompt when overwriting an existing .ico file." +
                          " 1 always overwrites, 0 always skips"), type=int, choices=[1,0])

args=parser.parse_args()


##--- Main ---##

# Icon Generation


for root, dirs, files in os.walk(args.input):
    for folder in dirs:
        #print(os.path.join(root,folder))
        convert_first_image(os.path.join(root,folder))

# Top Level
convert_first_image(args.input)

if args.iconsonly:
    print("done")
    sys.exit()



# Icon Assignment

# Remaining Directories
for root, dirs, files in os.walk(args.input):
    for folder in dirs:
        assign_icon(os.path.join(root,folder))

# Top Level
assign_icon(args.input)

print("done")
sys.exit()

            
            
