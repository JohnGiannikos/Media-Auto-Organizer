__author__ = 'john'

from scrappers import imdbpie
from persistance.db_schema import *
from .metadata import Metadata


class Imdb(Metadata):

    def update_metadata(self, *files):
        self.get_imdb_metadata(*files)

    def get_imdb_metadata(self,*files):
        imdb = imdbpie.Imdb()

        for media in files:
            media = media.media
            data = imdb.find_movie_by_id(media.imdbid)
            media.title = data.title
            media.tagline = data.tagline
            media.rating = data.rating
            media.year = data.year
            media.release_date = datetime.strptime(data.release_date, '%Y-%m-%d').date()
            media.plot_outline = data.plot_outline
            media.runtime = data.runtime
            media.cover_url = data.cover_url
            media.poster_url = data.poster_url


            for genre in data.genres:
                self.db.add_genre(media,genre)


            for director in data.directors_summary:
                self.db.add_person(media,director.name,'Director', director.imdb_id)

            for writer in data.writers_summary:
                self.db.add_person(media,writer.name,'Writer', writer.imdb_id)

            for cast in data.cast_summary:
                self.db.add_person(media,cast.name,'Cast', cast.imdb_id)

            if type(media) == Episode:
                series, is_new = self.db.create_series(data.data["series"]["tconst"])
                if is_new:
                    imdbdata = imdb.find_movie_by_id(series.imdbid)
                    series.tagline = imdbdata.tagline
                    series.title= imdbdata.title
                    series.rating= imdbdata.rating
                    series.year = imdbdata.year
                    series.plot_outline = imdbdata.plot_outline
                    series.cover_url = imdbdata.cover_url
                    series.poster_url = imdbdata.poster_url


                media.series = series