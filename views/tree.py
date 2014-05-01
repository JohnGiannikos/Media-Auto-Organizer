from collections import defaultdict
from persistance.db_schema import *
import math

class Folder(defaultdict):
    def __init__(self, *args, **kwargs):
        super(Folder, self).__init__(Folder)


class TreeView():

    def __init__(self, path, db):
        self.path = path
        self.db = db
        self.files = self.db.find_files()
        self.root=Folder()

    def import_view(self):
        pass

    def update_view(self):
        for file in self.files:
            if type(file.media) is Episode:
                self.insert_episode(file)
            elif type(file.media) is Movie:
                self.insert_movie(file)


    def insert_episode(self, file):

        media = file.media

        #Episode, common for all categories
        episode= {'link': file.path}

        #Create Series folder
        series = self.root["Series"]

        #---------Alphabetically
        alpha = series["Alphabetically"]
        letter = alpha[media.series.title[0]]
        series_folder = letter[media.series.title]
        season = series_folder[str(media.season)]
        season[str(media.episode_no)] = episode

        #--------By Series Year
        year = series["Series Year"]
        selected_year = year[str(media.series.year)]
        selected_year[media.series.title]= series_folder

        #------Episode Year
        eyear = series["Episode Year"]
        selected_eyear = eyear[str(media.year)]
        eyear_series_folder = selected_eyear[media.series.title]
        eyear_season=eyear_series_folder[str(media.season)]
        eyear_season[str(media.episode_no)]= episode

        #--------By Genre
        genre_folder = series["Genre"]
        for genre in media.genres:
            g = genre_folder[genre.name]
            g[media.series.title] = series_folder

        #-------By Rating
        byrating = series["Rating"]
        rating_folder = byrating[math.floor(media.series.rating)]
        rating_folder[media.series.title] = series_folder

        #------All
        all_folder = series["All"]
        all_folder[media.series.title] = series_folder

    def insert_movie(self,file):

        media = file.media

        #Episode, common for all categories
        movie= {'link': file.path}

        #Create Movies folder
        movies = self.root["Movies"]

        #---------Alphabetically
        alpha = movies["Alphabetically"]
        letter = alpha[media.title[0]]
        letter[media.title] = movie

        #--------By Movie Year
        year = movies["Year"]
        selected_year = year[str(media.year)]
        selected_year[media.title]= movie

        #--------By Genre
        genre_folder = movies["Genre"]
        for genre in media.genres:
            g = genre_folder[genre.name]
            g[media.title] = movie

        #-------By Rating
        byrating = movies["Rating"]
        rating_folder = byrating[math.floor(media.rating)]
        rating_folder[media.title] = movie

        #--------All
        all_movies = movies["All"]
        all_movies[media.title] = movie
