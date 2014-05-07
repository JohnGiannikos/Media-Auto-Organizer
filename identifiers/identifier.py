__author__ = 'john'

from abc import ABC, abstractmethod
import os
import mimetypes
import logging

class Identifier(ABC):

    def __init__(self, db):
        self.db = db

    @abstractmethod
    def get_identified_files(self):pass

    @abstractmethod
    def get_new_files(self):pass

    @abstractmethod
    def get_unidentified_files(self):pass

    @abstractmethod
    def identify_files(self,*file):pass

    def get_filetype(self, path):

        if not os.path.isfile(path):
            logging.error("This is not a file:" + path )
            return False

        if self.is_video(path):
            return 'video'
        else:
            logging.info("File " + path + " has unknown extension. Guessing mime type")
            fileMimeType, encoding = mimetypes.guess_type(path)
            if fileMimeType == None:
                return False
            fileMimeType = fileMimeType.split('/', 1)
            return fileMimeType[0]

    def is_video(self, path):

        fileExtension = path.rsplit('.', 1)
        if len(fileExtension)==1:
            return False
        if fileExtension[1]  in ['3g2', '3gp', '3gp2', '3gpp', 'ajp', \
        'asf', 'asx', 'avchd', 'avi', 'bik', 'bix', 'box', 'cam', 'dat', \
        'divx', 'dmf', 'dv', 'dvr-ms', 'evo', 'flc', 'fli', 'flic', 'flv', \
        'flx', 'gvi', 'gvp', 'h264', 'm1v', 'm2p', 'm2ts', 'm2v', 'm4e', \
        'm4v', 'mjp', 'mjpeg', 'mjpg', 'mkv', 'moov', 'mov', 'movhd', 'movie', \
        'movx', 'mp4', 'mpe', 'mpeg', 'mpg', 'mpv', 'mpv2', 'mxf', 'nsv', \
        'nut', 'ogg', 'ogm', 'ogv', 'omf', 'ps', 'qt', 'ram', 'rm', 'rmvb', \
        'swf', 'ts', 'vfw', 'vid', 'video', 'viv', 'vivo', 'vob', 'vro', \
        'webm', 'wm', 'wmv', 'wmx', 'wrap', 'wvx', 'wx', 'x264', 'xvid']:
            return True
        else:
            logging.info("This file is not a video (unknown mimetype AND invalid file extension):\n<i>" + path + "</i>")
            return False


