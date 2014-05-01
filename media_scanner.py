__author__ = 'john'

import os
import logging

from identifiers import opensubtitles
from metadata import imdb
from views.tree import TreeView

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

    def filter_old(self):
        self.files = [f for f in self.files if len(self.db.find_files(path=f.path))==0]

    def filter_video(self):
        self.files = [f for f in self.files if self.identifier.get_filetype(f.path)=='video']

    def analyze_files(self):
        logging.info("Recongnizing files")
        #recognize
        recognized , new = self.identifier.identify_files(*self.files)
        logging.info("Get more metadata")
        self.metadata.update_metadata(*new)
        for file in recognized:
            self.db.save_file(file)

        fs = TreeView('/home/john/mount', self.db)
        fs.update_view()
        fs = fs




if __name__ == "__main__":
    pass


