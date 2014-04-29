__author__ = 'john'

import os

from opensubtitles import OpenSubtitles
from db_schema import *
import logging
import imdbpie
import mimetypes
from _datetime import datetime

class MediaScanner():

    def __init__(self,db):
        self.db = db
        self.paths = list()
        self.files = list()

    def analyze_video(self ):

        with OpenSubtitles() as op:
            opinfo = op.get_video_info(*[(x,x.path) for x in self.paths])

        for v in opinfo:
            try :
                metadata=self.extract_opensubtitles_data(v)

                file.path = v["path"]
                self.files.append(file)
            except TypeError as e:
                logging.error("Error extracting data from opensubtitles" + str(e))
                continue

    def extract_opensubtitles_data(self, data):
        if data["MovieKind"] == "episode":
            return self.db.create_episode(imdbid="tt"+data["MovieImdbID"],
                                         season=int(data["SeriesSeason"]),
                                         episode_no=int(data["SeriesEpisode"]),
                                         year=int(data["MovieYear"]))
        elif data["MovieKind"] ==  "movie":
            return self.db.create_movie(imdbid="tt"+data["MovieImdbID"],
                                             year=int(data["MovieYear"]))
        else:
            raise TypeError("uknown video type")


    def update_metadata_imdb(self):
        imdb = imdbpie.Imdb()

        for file in self.files:
            data = imdb.find_movie_by_id(file.imdbid)
            file.title = data.title
            file.tagline = data.tagline
            file.rating = data.rating
            file.year = data.year
            file.release_date = datetime.strptime(data.release_date, '%Y-%m-%d').date()
            file.plot_outline = data.plot_outline
            file.runtime = data.runtime
            file.cover_url = data.cover_url
            file.poster_url = data.poster_url


            for genre in data.genres:
                self.db.add_genre(file,genre)


            for director in data.directors_summary:
                self.db.add_person(file,director.name,'Director', director.imdb_id)

            for writer in data.writers_summary:
                self.db.add_person(file,writer.name,'Writer', writer.imdb_id)

            for cast in data.cast_summary:
                self.db.add_person(file,cast.name,'Cast', cast.imdb_id)

            if type(file) == Episode:
                series = self.db.create_series(data.data["series"]["tconst"], data.data["series"]["title"],
                                            data.data["series"]["year"],  data.data["series"]["image"]["url"])
                file.series = series

            self.db.save_file(file)

    def scan_all_files_under_folder(self,path,minSize=0,ignoreExistingFiles=True):

        self.paths = list()

        for root, subFolders, files in os.walk(path):
            if files:
                for file in files:
                    full_path = os.path.join(root,file)
                    rec = self.db.create_file(path = full_path,
                                              size = os.stat(full_path).st_size)
                    if rec.size>= minSize:
                        self.paths.append(rec)
        logging.info("Found %d files" % len(self.paths))

    def filter_video(self):
        self.paths = [x for x in self.paths if get_filetype(x)=='video']

    def analyze_files(self):
        logging.info("Recongnizing files")
        self.analyze_video()
        logging.info("Get more metadata")
        self.update_metadata_imdb()

def get_filetype(path):

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


