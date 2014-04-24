__author__ = 'john'
import logging

from db_schema import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy.exc import IntegrityError

from datetime import datetime



class Database():

    def __init__(self):
        self.engine = create_engine('sqlite:///test.db', echo=True)
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()




    def create_episode(self,episode):
        pass

    def create_movie(self, movie):
        title = movie["info"]

        if title.type == 'tv_episode':
            raise IsEpisode()
        #General Info
        rec =  Movie(path=movie["path"], imdbid=title.imdb_id,title=title.title, rating=title.rating, year=title.year ,
                    tagline=title.tagline, release_date=datetime.strptime(title.release_date,'%Y-%m-%d').date(),
                    plot_outline=title.plot_outline,runtime=title.runtime, cover_url=title.cover_url)

        #Genre
        for genre in title.genres:
            new_genre,_ = self.get_or_create(Genre,name=genre)
            asc = GenreM2M()
            asc.genre = new_genre
            rec.genres.append(asc)

        #Directors
        director_job,_= self.get_or_create(Job,description="Director")
        for director in title.directors_summary:
            asc =  self.create_person_association(director,director_job)
            rec.persons.append(asc)

        #Writers
        writer_job,_= self.get_or_create(Job,description="Writer")
        for writer in title.directors_summary:
            asc =  self.create_person_association(writer,writer_job)
            rec.persons.append(asc)

        #Cast
        cast_job,_= self.get_or_create(Job,description="Cast")
        for cast in title.cast_summary:
            asc =  self.create_person_association(cast,cast_job)
            rec.persons.append(asc)


        return rec


    def create_person_association(self, person,job):
        person,_ = self.get_or_create(Person,imdbid=person.imdb_id, name=person.name)
        asc = PersonM2M()
        asc.job = job
        asc.person= person
        return asc


    def save_movie(self,*movies):
        for movie in movies:
            try:
                rec = self.create_movie(movie)
                self.session.add(rec)
                self.session.commit()
                rec = self.create_movie(movie)
                self.session.add(rec)
                self.session.commit()
            except IntegrityError as e:
                logging.warning("Movie with imdbid:" + movie["imdbid"]+ " exists")
                self.session.rollback()
            except IsEpisode:
                logging.warning("Movie with imdbid:" + movie["imdbid"]+ " is classified as movie but it is episode")
                self.create_episode(movie)




    def get_or_create(self, model, defaults=None, **kwargs):
        instance = self.session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance, False
        else:
            params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
            params.update(defaults or {})
            instance = model(**params)
            self.session.add(instance)
            return instance, True


"""-----------------------------Exceptions---------------------"""

class IsEpisode(Exception): pass
class IsMovie(Exception): pass


if __name__ == "__main__":
    pass


