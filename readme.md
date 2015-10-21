# Multi GoPro SD Importer
For use with 360 GoPro camera rigs of any size!
##How to setup...
###SD Importer Script
Add imp to your .bashrc eg:
    alias imp="cd path-to-the-repo/multiSDImportManager/gopro_import_script/ && ./imp"
It has to be done this way unless you want to move the config file to your root... it looks dumb but it works
### Pluraleyes to Final Cut Pro to CSV
Create a new Service in automator. Then copy and paste the code from lmx into a Run Shell Script module. Change the shell to usr/bin/python and the Pass Input field to 'as arguments'. Save it as something (lmx) and then when you right click on a .xml file generated in the PROJECTS directory and click services/lmx. This will result in a csv of the frame offset being made in the PROJECTS directory that you can use to sync videos in VideoStitch or AutoPano. AutoPano uses the inverted frame offsets, idk what VideoStitch uses.
## How to use...
Running
    imp C28 C34 C23 C43 C02 C33 C44 C65
will grab all footage of SD cards named C28, C34, C23, C43, C02, etc and drop them all in a chosen directory. If all cards are in alphanumeric order based inline with the arrangement of the camera cradles in the rig (eg Postion 1 = Card1, Position 2 = Card 2...) then just run imp
