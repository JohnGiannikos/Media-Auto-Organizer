from xmlrpc.client import ServerProxy, Error

import struct
import os
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



    def get_video_info(self, *paths):

        hashes = [self.hash(x) for x in paths]

        found_info = self.server.CheckMovieHash(self.session["token"], hashes)

        info = dict()

        for i,h in enumerate(hashes):
            if h in found_info["data"] and type(found_info["data"][h]) is dict:
                info[paths[i]] = found_info["data"][h]
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