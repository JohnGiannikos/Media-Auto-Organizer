__author__ = 'john'

import os
import logging
import data_types
from persistance import db_schema
from identifiers import opensubtitles
from metadata_finders import imdb

logging = logging.getLogger(__name__)

class MediaScanner():

    def __init__(self,db):
        self.db = db
        self.identifier = opensubtitles.Opensubtitles()
        self.metadata = imdb.Imdb(self.db)
        self.files = list()

    def scan_all_files_under_folder(self,path,minSize=0,ignoreExistingFiles=True):
        logging.info("Starting filescanning at %s"% path)
        for root, subFolders, files in os.walk(path):
            if files:
                for file in files:
                    full_path = os.path.join(root,file)
                    rec = data_types.File(path = full_path,
                                              size = os.stat(full_path).st_size)
                    if rec.size>= minSize:
                        self.files.append(rec)
        logging.info("Found %d files" % len(self.files))

    def filter_old(self):
        self.files = [f for f in self.files if len(self.db.find_files(path=f.path))==0]

    def filter_video(self):
        self.files = [f for f in self.files if self.identifier.get_filetype(f.path)=='video']

    def analyze_files(self):
        #recognize

        logging.info("Starting media recognition")
        recognized = self.identifier.identify_files(*self.files)
        logging.info("Recongnized %d media" % len(recognized))

        for file in recognized:
            media = file.media
            logging.info("Inserting file : %s" % file.path)

            if type(media) is data_types.Movie and not self.db.query(db_schema.Movie, imdbid=media.imdbid):
                logging.info('Movie is new, getting metadata')
                try:
                    self.metadata.update_metadata(file)
                except LookupError:
                    logging.error("Media recognized but could not get metadata : %s" % file.path)
                    continue
            elif type(media) is data_types.Episode and not self.db.query(db_schema.Episode, imdbid=media.imdbid):
                logging.info('Episode is new, getting metadata')
                try:
                    self.metadata.update_metadata(file)
                except LookupError:
                    logging.error("Media recognized but could not get metadata : %s" % file.path)
                    continue
            else:
                logging.info('Media exists, fetching metadata from db')
                media.load_from_db(self.db)

            file_db=file.create_db_object(self.db)
            self.db.save_file(file_db)

