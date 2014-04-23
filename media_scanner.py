__author__ = 'john'

import os
import sys
import logging


from opensubtitles import OpenSubtitles
from imdbpie import Imdb

root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)

class FilesScanner():

    def __init__(self):
        pass

    def scan_folder(self,path,minSize=0):
        files = self.get_all_files(path)

        filtered = [x["path"] for x in files if x["size"] >= minSize]

        with OpenSubtitles() as op:
            info = op.get_video_info(*filtered)

        return info


    def get_all_files(self, path):
        files_found = list()

        for root, subFolders, files in os.walk(path):
            if files:
                for file in files:
                    full_path = os.path.join(root,file)
                    rec = {"path" : full_path,
                           "size" : os.stat(full_path).st_size
                    }
                    files_found.append(rec)
        return files_found


if __name__ == "__main__":
    scanner = FilesScanner()
    files = scanner.scan_folder("/home/john/test movies",1*8*1024*1024)
    imdb = Imdb()
    movie = imdb.find_movie_by_id(files[0]["imdbid"])
    print(movie)

