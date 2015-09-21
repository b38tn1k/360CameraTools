import time
import os
import pickle
from SD import *


class ImportManager(object):
    def __init__(self, cards):
        self.load_config()
        self.time = time.strftime("%a %d %b %Y %H:%M", time.localtime())
        self.dump_count += 1
        self.user_input = ''
        # Collect new information
        self.user_input = raw_input('Shoot location:\nENTER to continue with {!s}\n'.format(self.location))
        if self.user_input != '':
            self.location = self.user_input
            self.dump_count = 1
            self.location = self.location.replace(' ', '_')
        self.user_input = ''
        self.user_input = raw_input('Path to Storage:\nENTER to continue with {!s}\n'.format(self.output_path))
        if self.user_input != '':
            self.output_path = self.user_input
        self.user_input = ''
        # create SD card objects
        self.sd_list = []
        for i, card in enumerate(cards):
            self.sd_list.append(SD(i, card))
        # grab any Notes
        while self.user_input != "x":
            for sd in self.sd_list:
                self.user_input = raw_input('Notes regarding {!s} or {!s}:\nEnter x to finish making notes\n'.format(sd.name, sd.camera))
                if self.user_input == "x":
                    break
                else:
                    sd.notes = self.user_input
        # Output
        self.export_directory = ''
        self.create_export_directory()
        for sd in self.sd_list:
            print "Copying from {!s}".format(sd.name)
            sd.copy_video(self.export_directory)
        self.export_txt()
        print "Copying Complete!\n"
        print "Shoot Location: {!s}".format(self.location)
        print "Shoot Number: {!s}".format(self.dump_count)
        print "Time: {!s}".format(self.time)
        for sd in self.sd_list:
            print "Camera: {!s}\tCard: {!s}\tNotes: {!s}".format(sd.camera, sd.name, sd.notes)
            for video_file in sd.files:
                print "File: {!s}".format(video_file)
        self.save_config()

    def create_export_directory(self):
        self.export_directory = os.path.join(self.output_path, self.location + '_' + str(self.dump_count))
        os.mkdir(self.export_directory)

    def save_config(self):
        file_object = open('importHelperConfig', 'wb')
        pickle.dump(self.location, file_object)
        pickle.dump(self.output_path, file_object)
        pickle.dump(self.dump_count, file_object)
        file_object.close()

    def load_config(self):
        file_object = open('importHelperConfig', 'r')
        self.location = pickle.load(file_object)
        self.output_path = pickle.load(file_object)
        self.dump_count = pickle.load(file_object)
        file_object.close()

    def export_txt(self):
        with open('{!s}/{!s}_{!s}.csv'.format(self.export_directory, self.location, self.dump_count), 'wb') as file_object:
            file_object.write("{!s}, {!s}, {!s}\n".format(self.location, self.time, 'Data Dump '+ str(self.dump_count)))
            file_object.write("FILE NAME, ORIGIN CAMERA, ORIGIN SD, NOTES\n")
            for sd in self.sd_list:
                for video_file in sd.files:
                    file_object.write("{!s}, {!s}, {!s}, {!s}\n".format(sd.camera + '_' + video_file, sd.camera, sd.name, sd.notes))
        file_object.close()
