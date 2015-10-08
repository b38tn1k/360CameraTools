import time
import os
import pickle
from SD import *
from threading import Thread, activeCount


class ImportManager(object):
    def __init__(self, cards, more):
        # self.location = 'Day 2 Cascades'
        # self.output_path = '/Volumes/TA_VR_M1/Northern_Territory/Katherine/'
        # self.import_count = 1
        # self.camera_rig = '11 Cam Drone Rig'
        # self.start_camera = 0

        self.load_config()
        self.more = more
        self.time = time.strftime("%a %d %b %Y %H:%M", time.localtime())
        if not self.more:
            self.import_count += 1
            self.start_camera = 0
        self.user_input = ''

        # more hacks...
        for card_name in cards:
            new_sd = True
            for card_id in self.sd_history:
                if card_name == card_id[0]:
                    card_id[1] += 1
                    print 'Card {!s} has been used {!s} times'.format(card_id[0], card_id[1])
                    new_sd = False
            if new_sd:
                self.sd_history.append([card_name, 0])


        # /more hacks...

        # create SD card objects
        self.sd_list = []
        for i, card in enumerate(cards):
            self.sd_list.append(SD(i + self.start_camera, card))
        self.start_camera = len(self.sd_list)
        # Collect new information
        self.user_input = raw_input('Shoot location:\nENTER to continue with {!s}\n'.format(self.location))
        if self.user_input != '':
            self.location = self.user_input
            self.import_count = 1
            self.location = self.location.replace(' ', '_')
        self.user_input = ''
        self.user_input = raw_input('Path to Storage 1:\nENTER to continue with {!s}\n'.format(self.output_path))
        if self.user_input != '':
            self.output_path = self.user_input
        self.user_input = ''
        self.user_input = raw_input('Camera Rig:\nENTER to continue with {!s}\n'.format(self.camera_rig))
        if self.user_input != '':
            self.camera_rig = self.user_input
        # grab any Notes
        while self.user_input != "x":
            for sd in self.sd_list:
                self.user_input = raw_input('Notes regarding {!s} or {!s}:\nEnter x to finish making notes\n'.format(sd.name, sd.camera))
                if self.user_input == "x":
                    break
                else:
                    sd.notes = self.user_input
        # Output_1
        self.export_directory = ''
        self.create_export_directory(self.output_path)
        sd_counter = 0
        start_time = time.time()
        for sd in self.sd_list:
            print "Copying from {!s}".format(sd.name)
            #sd.copy_video(self.export_directory, self.import_count, self.location) # THREAD THIS!!!
            sd_counter += 1

            # Cam_10_C01_F1_Day_1_Katherine_Gorge_Rock_Art_GOPR0030.MP4
            # def copy_video(self, export_directory, identifier, location):

            t = Thread(target=sd.copy_video, args =[self.export_directory, self.camera_rig, self.location]).start() # THREAD THIS!!!
            #Limit the number of concurrent threads
            while activeCount() >= 5:
                time.sleep(10)
                print('\033[94m'+"Waiting for active copy threads to finish. On sd #{}, with {} active threads, it has been {} seconds".format(sd_counter, activeCount(), time.time()-start_time) + '\033[0m')
            while(activeCount() > 1):
                time.sleep(10)
                print('\033[94m'+"Waiting for active copy threads to finish. On sd #{}, with {} active threads, it has been {} seconds".format(sd_counter, activeCount(), time.time()-start_time) + '\033[0m')

        self.export_csvs()

        print "Copying Complete!\n"
        print "Shoot Location: {!s}".format(self.location)
        print "Shoot Number: {!s}".format(self.import_count)
        print "Time: {!s}".format(self.time)
        for sd in self.sd_list:
            print "Camera: {!s}\tCard: {!s}\tNotes: {!s}\n".format(sd.camera, sd.name, sd.notes)
            for video_file in sd.files:
                print "File: {!s}".format(video_file.name)
                print "Duration: {!s}\nCreation Time: {!s}\nFrame Rate: {!s}\tBitrate: {!s}\nResolution: {!s}\n".format(video_file.duration, video_file.creation_time, video_file.frame_rate, video_file.bitrate, video_file.resolution)
        self.save_config()
        for sd in self.sd_list:
            os.system('diskutil umountDisk {!s}'.format(sd.name))

    def create_export_directory(self, output_path):
        self.export_directory = os.path.join(output_path, self.camera_rig + '_' + self.location + str(self.import_count))
        if not self.more and not os.path.exists(self.export_directory):
            os.mkdir(self.export_directory)

    def save_config(self):
        file_object = open('importHelperConfig', 'wb')
        pickle.dump(self.location, file_object)
        pickle.dump(self.output_path, file_object)
        pickle.dump(self.import_count, file_object)
        pickle.dump(self.camera_rig, file_object)
        pickle.dump(self.start_camera, file_object)
        pickle.dump(self.sd_history, file_object)
        file_object.close()

    def load_config(self):
        file_object = open('importHelperConfig', 'r')
        self.location = pickle.load(file_object)
        self.output_path = pickle.load(file_object)
        self.import_count = pickle.load(file_object)
        self.camera_rig = pickle.load(file_object)
        self.start_camera = pickle.load(file_object)
        self.sd_history = pickle.load(file_object)
        file_object.close()

    def export_csvs(self):
        file_name = '{!s}/{!s}_{!s}{!s}.csv'.format(self.export_directory, self.camera_rig, self.location, str(self.import_count))
        with open(file_name, 'a') as file_object:
            if not self.more:
                file_object.write("{!s}, {!s}, {!s}, {!s}\n".format(self.location, self.time, 'Shoot Number ' + str(self.import_count), self.camera_rig))
                file_object.write("FILE NAME, ORIGIN CAMERA, ORIGIN SD, CREATION TIME, DURATION, FRAME RATE, BITRATE, RESOLUTION, NOTES\n")
            for sd in self.sd_list:
                for video_file in sd.files:
                    file_object.write("{!s}, {!s}, {!s}, {!s}, {!s}, {!s}, {!s}, {!s}\n".format(sd.camera +'_'+self.camera_rig+'_'+ self.location + '_' + video_file.name, sd.camera, sd.name, video_file.creation_time, video_file.duration, video_file.frame_rate, video_file.bitrate, video_file.resolution, sd.notes))
        file_object.close()


# Forward Facing Camera Marked
# Concatenation via ffmpeg
# STATE/LOCATION/SHOOT_DAY/CAMERA/ROLL
# CAMERA = RIG (for VR stuff)
