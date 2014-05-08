__author__ = 'john'

from scrappers import imdbpie
import data_types
from .metadata import Metadata
from datetime import datetime

class Imdb(Metadata):

    def update_metadata(self, file):
        self.get_imdb_metadata(file)

    def get_imdb_metadata(self, file):
        imdb = imdbpie.Imdb()

        media = file.media
        data = imdb.find_movie_by_id(media.imdbid)
        media.title = data.title
        media.tagline = data.tagline
        media.rating = data.rating
        media.year = data.year
        try:
            media.release_date = datetime.strptime(data.release_date, '%Y-%m-%d').date()
        except TypeError:
            pass

        media.plot_outline = data.plot_outline
        media.runtime = data.runtime
        media.cover_url = data.cover_url
        media.poster_url = data.poster_url


        for genre in data.genres:
            new_genre = data_types.Genre(name=genre)
            media.genres.append(new_genre)

        for director in data.directors_summary:
            job = data_types.Job(description='Director')
            new_person = data_types.Person(imdbid= director.imdb_id, name=director.name, job=job)
            media.persons.append(new_person)

        for writer in data.writers_summary:
            job = data_types.Job(description='Writer')
            new_person = data_types.Person(imdbid= writer.imdb_id, name=writer.name, job=job)
            media.persons.append(new_person)

        for cast in data.cast_summary:
            job = data_types.Job(description='Cast')
            new_person = data_types.Person(imdbid= cast.imdb_id, name=cast.name, job=job)
            media.persons.append(new_person)

        if type(media) == data_types.Episode:
            series_imdb = data.data["series"]["tconst"]
            imdbdata = imdb.find_movie_by_id(series_imdb)
            new_series = data_types.Series( imdbid= series_imdb, tagline=imdbdata.tagline, title=imdbdata.title,
                                       rating= imdbdata.rating, year=imdbdata.year,plot_outline=imdbdata.plot_outline,
                                       cover_url=imdbdata.cover_url,poster_url=imdbdata.poster_url )

            media.series = new_series