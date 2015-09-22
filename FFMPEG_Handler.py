import subprocess as sp


class FFMPEG_Handler(object):
    def __init__(self, video_file):
        self.FFMPEG_BIN = "ffmpeg"
        self.infos = ''
        self.video_file = video_file

    def get_video_info(self):
        command = [self.FFMPEG_BIN,'-i', self.video_file, '-']
        pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.PIPE)
        pipe.stdout.readline()
        self.infos = pipe.stderr.read()
        pipe.terminate()

    def digest_infos(self):
        pass

fh = FFMPEG_Handler('my_video.mp4')
fh.get_video_info()
fh.digest_infos()
