import shutil
import os

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
                self.files.append(file_object)

    def copy_video(self, export_directory):
        i = 1
        for file_object in self.files:
            full_origin = os.path.join(self.path, file_object)
            print "Copying File {!s} of {!s}".format(i, len(self.files))
            full_destination = os.path.join(export_directory, "{!s}_{!s}".format(self.camera, file_object))
            shutil.copyfile(full_origin, full_destination)
            i += 1
