# 360 Camera Tools
Data management scripts for 360 Cameras
##Requirements

    brew install ffmpeg --with-fdk-aac --with-ffplay --with-freetype --with-frei0r --with-libass --with-libvo-aacenc --with-libvorbis --with-libvpx --with-opencore-amr --with-openjpeg --with-opus --with-rtmpdump --with-schroedinger --with-speex --with-theora --with-tools

##How to setup...
###SD Importer Script
Add imp to your .bashrc eg:

    alias imp="cd /path-to-the-imp && ./imp"
It has to be done this way unless you want to move the config file to your bin... it looks dumb but it works.
###Lazy Concat Script
Currently I am just dropping the concat script into my /usr/local/bin and running:

    concat .
whilst in the directory containing the files I wish to concatenate.
###Pluraleyes to Final Cut Pro to CSV
Create a new Service in automator. Then copy and paste the code from lmx into a Run Shell Script module. Change the shell to usr/bin/python and the Pass Input field to 'as arguments'. Save it as something (lmx) and then when you right click on a .xml file generated in the PROJECTS directory and click services/lmx. This will result in a csv of the frame offset being made in the PROJECTS directory that you can use to sync videos in VideoStitch or AutoPano. AutoPano uses the inverted frame offsets, idk what VideoStitch uses. An example workflow is provided.
## How to use...
To import video files from the cards:

    imp C28 C34 C23 C43 C02 C33 C44 C65
will grab all footage of SD cards named C28, C34, C23, C43, C02, etc and drop them all in a chosen target directory. If all cards are in alphanumeric order based inline with the arrangement of the camera cradles in the rig (eg Position 1 = Card1, Position 2 = Card 2...) then you can just run imp. While loading cards it is sometimes useful to stay in command line and update your imp command as you load the cards. For this purpose, running

    imp -lsvol
in a separate window can be helpful.
For more info:

    imp -h
###Other Useful Things
In combination with these tools, I reccomend installing [iTerm2](https://www.iterm2.com/) and [htop](http://hisham.hm/htop/):

    brew install htop
