__author__ = 'john'


import logging
from .identifier import Identifier
from scrappers import opensubtitles
import data_types

class Opensubtitles(Identifier):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_files = None
        self.recognized_files = None
        self.new_files = None

    def identify_files(self, *files):
        #break in smaller groups
        groupslist = [files[i:i+50] for i in range(0, len(files), 50)]

        recognized_list = list()

        for group in groupslist:
            new = self.identify_video(*group)
            recognized_list.extend(new)

        return recognized_list


    def identify_video(self, *files):

            with opensubtitles.OpenSubtitles() as op:
                osinfo = op.get_video_info(*[x.path for x in files])

            recognized = list()

            for f in files:
                if f.path in osinfo:
                    try:
                        f.media = self.extract_opensubtitles_data(osinfo[f.path])
                        recognized.append(f)
                    except TypeError as e:
                        logging.error("Error extracting data from opensubtitles" + str(e))
                        continue

            return recognized

    def extract_opensubtitles_data(self, data):
        if data["MovieKind"] == "episode":
            return data_types.Episode(imdbid="tt"+data["MovieImdbID"],
                                         season=int(data["SeriesSeason"]),
                                         episode_no=int(data["SeriesEpisode"]),
                                         year=int(data["MovieYear"]))
        elif data["MovieKind"] ==  "movie":
            return data_types.Movie(imdbid="tt"+data["MovieImdbID"],
                                             year=int(data["MovieYear"]))
        else:
            raise TypeError("uknown video type")

