__author__ = 'john'

import os
import logging

from identifiers import opensubtitles
from metadata import imdb

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
        #recognize

        recognized = self.identifier.identify_files(*self.files)
        new = self.identifier.get_new_files()

        for file in recognized:
            logging.info("Inserting file : %s" % file.path)
            if file in new:
                self.metadata.update_metadata(file)
            self.db.save_file(file)



if __name__ == "__main__":
    pass


