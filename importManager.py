import time
import os
import pickle
from SD import *
from threading import Thread, activeCount


class ImportManager(object):
    def __init__(self, cards, more):
        self.load_config()
        self.more = more
        self.time = time.strftime("%a %d %b %Y %H:%M", time.localtime())
        if not self.more:
            self.take_count += 1
            self.start_camera = 0
        self.user_input = ''
        # Collect new information
        self.user_input = raw_input('Shoot location:\nENTER to continue with {!s}\n'.format(self.location))
        if self.user_input != '':
            self.location = self.user_input
            self.take_count = 1
            self.location = self.location.replace(' ', '_')
        self.user_input = ''
        self.user_input = raw_input('Path to Storage:\nENTER to continue with {!s}\n'.format(self.output_path))
        if self.user_input != '':
            self.output_path = self.user_input
        self.user_input = ''
        self.user_input = raw_input('Camera Rig:\nENTER to continue with {!s}\n'.format(self.camera_rig))
        if self.user_input != '':
            self.camera_rig = self.user_input
        # create SD card objects
        self.sd_list = []
        for i, card in enumerate(cards):
            self.sd_list.append(SD(i + self.start_camera, card))
        self.start_camera = len(self.sd_list)
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
        sd_counter = 0
        start_time = time.time()
        for sd in self.sd_list:
            print "Copying from {!s}".format(sd.name)
            #sd.copy_video(self.export_directory, self.take_count, self.location) # THREAD THIS!!!
            sd_counter += 1
            t = Thread(target=sd.copy_video, args =[self.export_directory, self.take_count, self.location]).start() # THREAD THIS!!!
            #Limit the number of concurrent threads
            while activeCount() >= 3:
                time.sleep(1)
                print("Waiting for active copy threads to finish. On sd #{}, with {} active threads, it has been {} seconds".format(sd_counter, activeCount(), time.time()-start_time))
        while(activeCount() > 1):
            time.sleep(1)
            print("Waiting for active copy threads to finish. On sd #{}, with {} active threads, it has been {} seconds".format(sd_counter, activeCount(), time.time()-start_time))

        self.export_csvs()
        print "Copying Complete!\n"
        print "Shoot Location: {!s}".format(self.location)
        print "Shoot Number: {!s}".format(self.take_count)
        print "Time: {!s}".format(self.time)
        for sd in self.sd_list:
            print "Camera: {!s}\tCard: {!s}\tNotes: {!s}".format(sd.camera, sd.name, sd.notes)
            for video_file in sd.files:
                print "File: {!s}".format(video_file.name)
        self.save_config()
        for sd in self.sd_list:
            os.system('diskutil umountDisk {!s}'.format(sd.name))

    def create_export_directory(self):
        self.export_directory = os.path.join(self.output_path, self.location + '_Take_' + str(self.take_count))
        #if not self.more:
        if not self.more and not os.path.exists(self.export_directory):
            os.mkdir(self.export_directory)

    def save_config(self):
        file_object = open('importHelperConfig', 'wb')
        pickle.dump(self.location, file_object)
        pickle.dump(self.output_path, file_object)
        pickle.dump(self.take_count, file_object)
        pickle.dump(self.camera_rig, file_object)
        pickle.dump(self.start_camera, file_object)
        file_object.close()

    def load_config(self):
        file_object = open('importHelperConfig', 'r')
        self.location = pickle.load(file_object)
        self.output_path = pickle.load(file_object)
        self.take_count = pickle.load(file_object)
        self.camera_rig = pickle.load(file_object)
        self.start_camera = pickle.load(file_object)
        file_object.close()

    def export_csvs(self):
        # Master
        with open('{!s}/{!s}.csv'.format(self.output_path, self.location), 'a') as master_file:
            if not self.more:
                master_file.write("Take: {!s}, Location: {!s}, Time: {!s}, Rig: {!s}\n".format(str(self.take_count), self.location, self.time, self.camera_rig))
                master_file.write("FILE NAME, ORIGIN CAMERA, ORIGIN SD, CREATION TIME, DURATION, FRAME RATE, BITRATE, NOTES\n")
            for sd in self.sd_list:
                for video_file in sd.files:
                    master_file.write("{!s}, {!s}, {!s}, {!s}, {!s}, {!s}, {!s}, {!s}\n".format(sd.camera + '_Take_' + str(self.take_count) + '_' + self.location + '_' + video_file.name, sd.camera, sd.name, video_file.creation_time, video_file.duration, video_file.frame_rate, video_file.bitrate, sd.notes))
        master_file.close()
        # Specific
        with open('{!s}/{!s}_{!s}.csv'.format(self.export_directory, self.location, 'Take_' + str(self.take_count)), 'a') as file_object:
            if not self.more:
                file_object.write("{!s}, {!s}, {!s}, {!s}\n".format(self.location, self.time, 'Shoot Number ' + str(self.take_count), self.camera_rig))
                file_object.write("FILE NAME, ORIGIN CAMERA, ORIGIN SD, CREATION TIME, DURATION, FRAME RATE, BITRATE, NOTES\n")
            for sd in self.sd_list:
                for video_file in sd.files:
                    file_object.write("{!s}, {!s}, {!s}, {!s}, {!s}, {!s}, {!s}, {!s}\n".format(sd.camera + '_Take_' + str(self.take_count) + '_' + self.location + '_' + video_file.name, sd.camera, sd.name, video_file.creation_time, video_file.duration, video_file.frame_rate, video_file.bitrate, sd.notes))
        file_object.close()
