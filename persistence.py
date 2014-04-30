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
        self.session = Session(autocommit=False)

    def create_file(self,**kwargs):
        return File(**kwargs)

    def create_episode(self,**kwargs):
        episode,_ =  self.get_or_create(Episode, **kwargs)
        return episode

    def create_movie(self,**kwargs):
        movie,_ =  self.get_or_create(Movie, **kwargs)
        return movie

    def create_series(self,imdbid,title,year,image_url):
        series,_ =  self.get_or_create(Series, imdbid=imdbid, title=title, year=year, image_url=image_url)
        return series

    def add_person(self,file,name,job,imdbid=None):
        person,_ = self.get_or_create(Person, imdbid=imdbid, name=name)
        job, _ = self.get_or_create(Job, description=job)

        asc = PersonM2M()
        asc.job = job
        asc.person = person

        file.persons.append(asc)

    def add_genre(self,file,name):
        new_genre, _ = self.get_or_create(Genre, name=name)
        file.genres.append(new_genre)

    def save_file(self,file):
        try:
            self.session.add(file)
            self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
            logging.error("Error inserting file %s" % str(e))
            return


    def get_or_create(self, model, defaults=None, **kwargs):
        with self.session.no_autoflush:
            instance = self.session.query(model).filter_by(**kwargs).first()
            if instance:
                return instance, False
            else:
                params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
                params.update(defaults or {})
                instance = model(**params)
                self.session.add(instance)
                self.session.commit()
                return instance, True


"""-----------------------------Exceptions---------------------"""


class IsEpisode(Exception): pass


class IsMovie(Exception): pass


if __name__ == "__main__":
    pass


