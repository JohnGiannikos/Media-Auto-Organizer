__author__ = 'john'


import logging
from .identifier import Identifier
from scrappers import opensubtitles


class Opensubtitles(Identifier):

    def __init__(self, db):
        self.db = db

    def identify_files(self, *files):
        return self.identify_video(*files)


    def identify_video(self, *files):

            with opensubtitles.OpenSubtitles() as op:
                osinfo = op.get_video_info(*[x.path for x in files])

            recognized = list()
            new = list()
            for f in files:
                if f.path in osinfo:
                    try:
                        f.media, is_new = self.extract_opensubtitles_data(osinfo[f.path])
                        if is_new:
                            new.append(f)
                        recognized.append(f)
                    except TypeError as e:
                        logging.error("Error extracting data from opensubtitles" + str(e))
                        continue

            return recognized, new

    def extract_opensubtitles_data(self, data):
        if data["MovieKind"] == "episode":
            return self.db.get_episode(imdbid="tt"+data["MovieImdbID"],
                                         season=int(data["SeriesSeason"]),
                                         episode_no=int(data["SeriesEpisode"]),
                                         year=int(data["MovieYear"]))
        elif data["MovieKind"] ==  "movie":
            return self.db.get_movie(imdbid="tt"+data["MovieImdbID"],
                                             year=int(data["MovieYear"]))
        else:
            raise TypeError("uknown video type")

