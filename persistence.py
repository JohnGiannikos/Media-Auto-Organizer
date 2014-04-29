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

    def create_episode(self,**kwargs):
        return Episode(**kwargs)

    def create_movie(self,**kwargs):
        return Movie(**kwargs)

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
        asc = GenreM2M()
        asc.genre = new_genre
        file.genres.append(asc)


    def save_movies(self, *movies):
        for movie in movies:
            try:
                rec = self.create_movie_obj(movie)
                self.session.add(rec)
                self.session.commit()
            except IntegrityError as e:
                logging.warning("Movie with imdbid:" + movie["imdbid"] + " exists")
                self.session.rollback()
            except IsEpisode:
                logging.warning("Movie with imdbid:" + movie["imdbid"] + " is classified as movie but it is episode")
                self.session.rollback()
                self.save_episodes(movie)

    def save_episodes(self, *episodes):
        for episode in episodes:
            try:
                rec = self.create_episode_obj(episode)
                self.session.add(rec)
                self.session.commit()
            except IntegrityError as e:
                logging.warning("Episode with imdbid:" + episode["imdbid"] + "Integrity error: " + str(e))
                self.session.rollback()
            except IsMovie:
                logging.warning("Movie with imdbid:" + episode["imdbid"] + " is classified as movie but it is episode")
                self.session.rollback()
                #continue
                self.save_movies(episode)

    def save_file(self,file):
        self.session.add(file)
        self.session.commit()

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


