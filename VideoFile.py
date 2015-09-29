import subprocess as sp


class VideoFile(object):
    def __init__(self, name, path):
        self.FFMPEG_BIN = "ffmpeg"
        self.infos = ''
        self.name = name
        self.path = path
        self.analyse()
        self.digest_infos()

    def analyse(self):
        command = [self.FFMPEG_BIN,'-i', self.path, '-']
        pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.PIPE)
        pipe.stdout.readline()
        self.infos = pipe.stderr.read()
        pipe.terminate()

    def digest_infos(self):
        # print self.infos
        index = self.infos.find('creation_time   : ')
        self.creation_time = self.infos[index+len('creation_time   : '):index+len('creation_time   : ' )+len('2015-01-01 00:32:49')]
        index = self.infos.find('Duration: ')
        self.duration = self.infos[index+len('Duration: '):index+len('Duration: ')+len('00:06:07.47')]
        index = self.infos.find('bitrate: ')
        self.bitrate = self.infos[index+len('bitrate: '):index+len('bitrate: ')+len('60158 kb/s')]
        index = self.infos.find(' fps')
        self.frame_rate = self.infos[index-5:index]
        index = self.infos.find(' [SAR')
        self.resolution = self.infos[index-len('1920x1440'):index]
        # print 'Created: \t' + self.creation_time
        # print 'Duration: \t' + self.duration
        # print 'Bitrate: \t' + self.bitrate
        # print 'Frame Rate: \t' + self.frame_rate
        # print 'Resolution: \t' + self.resolution

    def concat(self, other_videos):
        for video in other_videos:
            pass
            new_video = '''this is where I concat'''
