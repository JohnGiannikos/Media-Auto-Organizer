__author__ = 'john'


import logging
from .identifier import Identifier
from scrappers import opensubtitles


class Opensubtitles(Identifier):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_files = None
        self.recognized_files = None
        self.new_files = None

    def identify_files(self, *files):
        #break in smaller groups
        self.all_files = files
        groupslist = [files[i:i+50] for i in range(0, len(files), 50)]

        recognized_list = list()
        new_list = list()
        for group in groupslist:
            all, new = self.identify_video(*group)
            recognized_list.extend(all)
            new_list.extend(new)

        self.recognized_files = recognized_list
        self.new_files = new_list
        return recognized_list

    def get_identified_files(self):
        return self.recognized_files


    def get_new_files(self):
        return  self.new_files


    def get_unidentified_files(self):
        unrecognized = list()
        for file in self.all_files:
            if file not in self.recognized_files:
                unrecognized.append(file)

        return unrecognized


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

