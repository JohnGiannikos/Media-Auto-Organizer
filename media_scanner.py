__author__ = 'john'

import os

from identifiers import opensubtitles
from metadata import imdb
import logging
import mimetypes

class MediaScanner():

    def __init__(self,db):
        self.db = db
        self.identifier = opensubtitles.Opensubtitles(self.db)
        self.metadata = imdb.Imdb(self.db)
        self.paths = list()
        self.files = list()

    def scan_all_files_under_folder(self,path,minSize=0,ignoreExistingFiles=True):

        self.paths = list()

        for root, subFolders, files in os.walk(path):
            if files:
                for file in files:
                    full_path = os.path.join(root,file)
                    rec = self.db.create_file(path = full_path,
                                              size = os.stat(full_path).st_size)
                    if rec.size>= minSize:
                        self.files.append(rec)
        logging.info("Found %d files" % len(self.paths))

    def filter_video(self):
        self.paths = [x for x in self.paths if get_filetype(x.path)=='video']

    def analyze_files(self):
        logging.info("Recongnizing files")
        #recognize
        recognized = self.identifier.analyze_video(*self.files)
        logging.info("Get more metadata")
        self.metadata.update_metadata(*recognized)




def get_filetype( path):

    if not os.path.isfile(path):
        logging.error("This is not a file:" + path )
        return False

    if is_video(path):
        return 'video'
    else:
        logging.info("File " + path + " has unknown extension. Guessing mime type")
        fileMimeType, encoding = mimetypes.guess_type(path)
        if fileMimeType == None:
            return False
        fileMimeType = fileMimeType.split('/', 1)
        return fileMimeType[0]

def is_video(path):

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








if __name__ == "__main__":
    pass


