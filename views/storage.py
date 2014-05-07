__author__ = 'john'

from persistance.db_schema import *
import views


class StorageView():

    def __init__(self, db):
        self.db = db
        self.root=views.Folder()

    def create_view(self, media_type=None, new_root_path=None):

        files = self.db.find_files()

        for file in files:
            if type(file.media) is Episode and (media_type == Episode or media_type is None):
                self.insert_episode(file)
            elif type(file.media) is Movie and (media_type == Movie or media_type is None):
                self.insert_movie(file)

    def insert_episode(self, file):

        media = file.media

        #Episode, common for all categories
        episode= [views.File(file)]

        #Create Series folder
        series = self.root["Series"]

        series_folder = series[media.series.title]
        season = series_folder['Season '+ str(media.season)]
        season[str(media.episode_no)] = episode

    def insert_movie(self,file):

        media = file.media
        #Movie, common for all categories
        movie= [views.File(file)]

        #Create Movies folder
        movies = self.root["Movies"]
        movies[media.title] = movie


