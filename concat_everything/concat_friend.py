import os
import time
from gopro_file_friend import *
import subprocess

#lossless mp4 concat script
#BASED PURELY ON THE BELIEF THAT LISTS TAKEDN FROM DIRECTORIES WILL ALWAYS BE IN ALPHANUMERIC ORDER CAUSE ...
#RISKY

def print_list(_list):
    for _item in _list:
        print _item

def build_concat_command(_list):
    print '\n'
    # print_list(ts.children)
    inner_str = _list[0]
    outpur_str = _list[0].strip('.ts') + '_concat'
    for child in _list[1:]:
        inner_str += '|' + child
    command = 'ffmpeg -i "concat:{!s}" -c copy -bsf:a aac_adtstoasc {!s}.mp4'.format(inner_str, outpur_str)
    return command

path = os.getcwd()
files = os.listdir(path)

# Convert into transport stream (file level transcode)
for video in files:
    if '.MP4' in video.upper():
        short_name = video.strip('.MP4')
        short_name = short_name.strip('.mp4')  # not sure. dum
        os.system('ffmpeg -i {!s}.MP4 -c copy -bsf:v h264_mp4toannexb -f mpegts {!s}.ts'.format(short_name, short_name))
        time.sleep(10)

files = os.listdir(path)
# Concat the transport streams and output as an mp4
one_really_long_command = ''
for video in files:
    if '.ts' in video and 'GOPR' in video:    # this is not case sensitive ergo shit
        short_name = video.strip('.ts')
        ts = GoProFriend(video)
        for child in files:
            if ts.cam in child and ts.event in child and '.ts' in child and not video in child: #bad james
                ts.add_child(child)
        command = build_concat_command(ts.children)
        # print command
        # subprocess.call(command)
        # subprocess.wait()
        # time.sleep(1)

        #WORST/BEST IDEA EVER!!!!
        one_really_long_command += command + '&&'
one_really_long_command += 'say complete'

os.system(one_really_long_command)


print '\n'
