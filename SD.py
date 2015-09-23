import shutil
import os
import hashlib
from VideoFile import *
import sys

class SD(object):
    def __init__(self, camera, card):
        self.number = card
        self.camera = "Cam_{!s}".format(camera+1)
        self.name = "C{!s}".format(str(self.number).zfill(2))
        self.notes = ""
        self.path = "/Volumes/{!s}/DCIM/100GOPRO".format(self.name)
        self.files = []
        list_dir = os.listdir(self.path)
        for file_object in list_dir:
            if '.MP4' in file_object.upper():
                full_origin = os.path.join(self.path, file_object)
                self.files.append(VideoFile(file_object, full_origin))

                # USE VIDEO CLASS ABOVE AND ADD ALL THE INFORMATION
                # MOVING TOWARDS AN APPEND METHOD

    def copy_video(self, export_directory, take_number, location):
        i = 1
        for file_object in self.files:
            checksum = self.md5(file_object.path)
            print "Copying File {!s} of {!s}".format(i, len(self.files))
            full_destination = os.path.join(export_directory, "{!s}_{!s}_{!s}_{!s}".format(self.camera, 'Take_' + str(take_number), location, file_object.name))
            shutil.copyfile(file_object.path, full_destination)
            checksum2 = self.md5(full_destination)
            if checksum2 != checksum:
                print "Error Copying {!s} to {!s}".format(file_object.path, full_destination)
                sys.stdout.write('\a')
                sys.stdout.flush()
            i += 1

    def md5(self, fname):
        hash = hashlib.md5()
        with open(fname) as f:
            for chunk in iter(lambda: f.read(4096), ""):
                hash.update(chunk)
        print 'md5 checksum: ' + hash.hexdigest()
        return hash.hexdigest()
