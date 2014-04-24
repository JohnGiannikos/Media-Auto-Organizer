from xmlrpc.client import ServerProxy, Error

import struct
import os
import mimetypes
import logging
import time

class OpenSubtitles():

    def __init__(self):
        self.server = ServerProxy('http://api.opensubtitles.org/xml-rpc')
        self.session = None
        self.login()

    def login(self):
        try:
        # Connection to opensubtitles.org server
            self.session = self.server.LogIn("buluba89","123456","en","organizemymovies")
        except Exception:
            # Retry once, it could be a momentary overloaded server?
            time.sleep(3)
            try:
                # Connection to opensubtitles.org server
                self.session = self.server.LogIn("buluba89","123456","en","organizemymovies")
            except Exception:
                # Failed connection attempts?
                logging.error( "Connection error!", "Unable to reach opensubtitles.org servers!")
                raise  ConnectionError()
        if self.session['status'] != '200 OK':
            logging.error( "Connection error!", "Opensubtitles.org servers refused the connection: " + self.session['status'])
            raise  ConnectionError()

    def logout(self):
        self.server.LogOut(self.session["token"])

    def hash(self,path):
        """Produce a hash for a video file: size + 64bit chksum of the first and
        last 64k (even if they overlap because the file is smaller than 128k)"""
        longlongformat = 'Q' # unsigned long long little endian
        bytesize = struct.calcsize(longlongformat)
        format = "<%d%s" % (65536//bytesize, longlongformat)

        f = open(path, "rb")

        filesize = os.fstat(f.fileno()).st_size
        hash = filesize

        if filesize < 65536 * 2:
            logging.error("error", "", "File size error while generating hash for this file:\n<i>" + path + "</i>")
            raise IOError()

        buffer = f.read(65536)
        longlongs = struct.unpack(format, buffer)
        hash += sum(longlongs)

        f.seek(-65536, os.SEEK_END) # size is always > 131072
        buffer = f.read(65536)
        longlongs = struct.unpack(format, buffer)
        hash += sum(longlongs)
        hash &= 0xFFFFFFFFFFFFFFFF

        f.close()
        returnedhash = "%016x" % hash
        return returnedhash


    def is_video(self,path):
        """Check mimetype and/or file extension to detect valid video file
            !!!!!!!!!!!mime guessing is slow!!!!!!!!!!
        """
        if os.path.isfile(path) == False:
            print("error", "", "This is not a file:\n<i>" + path + "</i>")
            return False

        #fileMimeType, encoding = mimetypes.guess_type(path)
        fileMimeType = None
        if fileMimeType == None:
            fileExtension = path.rsplit('.', 1)
            if fileExtension[1] not in ['3g2', '3gp', '3gp2', '3gpp', 'ajp', \
            'asf', 'asx', 'avchd', 'avi', 'bik', 'bix', 'box', 'cam', 'dat', \
            'divx', 'dmf', 'dv', 'dvr-ms', 'evo', 'flc', 'fli', 'flic', 'flv', \
            'flx', 'gvi', 'gvp', 'h264', 'm1v', 'm2p', 'm2ts', 'm2v', 'm4e', \
            'm4v', 'mjp', 'mjpeg', 'mjpg', 'mkv', 'moov', 'mov', 'movhd', 'movie', \
            'movx', 'mp4', 'mpe', 'mpeg', 'mpg', 'mpv', 'mpv2', 'mxf', 'nsv', \
            'nut', 'ogg', 'ogm', 'ogv', 'omf', 'ps', 'qt', 'ram', 'rm', 'rmvb', \
            'swf', 'ts', 'vfw', 'vid', 'video', 'viv', 'vivo', 'vob', 'vro', \
            'webm', 'wm', 'wmv', 'wmx', 'wrap', 'wvx', 'wx', 'x264', 'xvid']:
                logging.info("This file is not a video (unknown mimetype AND invalid file extension):\n<i>" + path + "</i>")
                return False
        else:
            fileMimeType = fileMimeType.split('/', 1)
            if fileMimeType[0] != 'video':
                logging.info( "This file is not a video (unknown mimetype):<i>" + path + "</i>")
                return False

        return True

    def get_video_info(self,*paths):
        video = list()
        for path in paths:
            if self.is_video(path):
                video.append({ "path" : path,
                               "hash" : self.hash(path)
                })

        found_info = self.server.CheckMovieHash(self.session["token"],[x["hash"] for x in video])

        info = list()

        for v in video:
            if v["hash"] in found_info["data"] and type(found_info["data"][v["hash"]]) is dict:
                tmp = {"path" : v["path"],
                       "imdbid" : "tt" + found_info["data"][v["hash"]]["MovieImdbID"] }

                info.append(tmp)
        return info

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()
        if exc_type:
            logging.error(exc_type)

if __name__ == "__main__":
    op = OpenSubtitles()
    op.logout()