import subprocess as sp


class FFMPEG_Handler(object):
    def __init__(self, video_file):
        self.FFMPEG_BIN = "ffmpeg"
        self.infos = ''
        self.video_file = video_file
        self.get_video_info()
        self.digest_infos()

    def get_video_info(self):
        command = [self.FFMPEG_BIN,'-i', self.video_file, '-']
        pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.PIPE)
        pipe.stdout.readline()
        self.infos = pipe.stderr.read()
        pipe.terminate()

    def digest_infos(self):
        print self.infos
        index = self.infos.find('creation_time   : ')
        self.creation_time = self.infos[index+len('creation_time   : '):index+len('creation_time   : ' )+len('2015-01-01 00:32:49')]
        index = self.infos.find('Duration: ')
        self.duration = self.infos[index+len('Duration: '):index+len('Duration: ')+len('00:06:07.47')]
        index = self.infos.find('bitrate: ')
        self.bitrate = self.infos[index+len('bitrate: '):index+len('bitrate: ')+len('60158 kb/s')]
        index = self.infos.find(' fps')
        self.frame_rate = str(int(self.infos[index-3:index]))
        print 'Created: \t' + self.creation_time
        print 'Duration: \t' + self.duration
        print 'Bitrate: \t' + self.bitrate
        print 'Frame Rate: \t' + self.frame_rate

fh = FFMPEG_Handler('Old_Pittwater_Road_Take_1/Cam_4_Take_1_Old_Pittwater_Road_GOPR9999.MP4')
fh.get_video_info()
fh.digest_infos()
