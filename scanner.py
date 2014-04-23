__author__ = 'john'

import os
import sys
import logging


from opensubtitles import OpenSubtitles

root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)

class FilesScanner():

    def __init__(self):
        pass

    def scanFolder(self,path,minSize=0):
        files = self.getAllFiles(path)

        filtered = [x["path"] for x in files if x["size"] >= minSize]

        op = OpenSubtitles()

        info = op.getVideoInfo(*filtered)

        op.logout()

        return info


    def getAllFiles(self,path):
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
    files = scanner.scanFolder("/home/john/test movies",1*8*1024*1024)
    print(files)

