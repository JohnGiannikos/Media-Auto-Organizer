__author__ = 'john'
import logging

from sqlalchemy import create_engine, Column, Integer, String , Float, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

Base = declarative_base()


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    type = Column("type", Integer)
    path = Column(String)
    genres = relationship("GenreM2M", backref="files")
    persons = relationship("PersonM2M", backref="files")

    __mapper_args__ = {'polymorphic_on': type}


class Movie(File):
    __tablename__ = 'movies'
    __mapper_args__ = {'polymorphic_identity': 1}
    movie_id = Column('id',Integer,ForeignKey('files.id'), primary_key=True)
    imdbid = Column(String, unique=True,primary_key=True)
    tagline = Column(String)
    title = Column(String)
    rating = Column(Float)
    year = Column(Integer)
    runtime = Column(String)
    release_date = Column(Date)
    plot_outline = Column(String)
    cover_url = Column(String)


class Genre(Base):
    __tablename__= 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class GenreM2M(Base):
    __tablename__='genre_m2m'
    file_id = Column(Integer, ForeignKey('files.id'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genres.id'), primary_key=True)
    genre = relationship("Genre", backref="file_assocs")

class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer,primary_key=True)
    imdbid = Column(String, unique=True)
    name = Column(String)

class PersonM2M(Base):
    __tablename__='person_m2m'
    id = Column(Integer,primary_key=True)
    file_id = Column(Integer, ForeignKey('files.id'))
    person_id = Column(Integer, ForeignKey('persons.id'))
    job_id = Column(Integer,ForeignKey('jobs.id'))
    job = relationship('Job')
    person = relationship("Person", backref="file_assocs")

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer,primary_key=True)
    description = Column(String)


def create_episode(session,episode):
    pass

def create_movie(session, movie):
    title = movie["info"]

    if title.type == 'tv_episode':
        raise IsEpisode()
    #General Info
    rec =  Movie(path=movie["path"], imdbid=title.imdb_id,title=title.title, rating=title.rating, year=title.year ,
                tagline=title.tagline, release_date=datetime.strptime(title.release_date,'%Y-%m-%d').date(),
                plot_outline=title.plot_outline,runtime=title.runtime, cover_url=title.cover_url)

    #Genre
    for genre in title.genres:
        new_genre,_ = get_or_create(session, Genre,name=genre)
        asc = GenreM2M()
        asc.genre = new_genre
        rec.genres.append(asc)

    #Directors
    director_job,_= get_or_create(session,Job,description="Director")
    for director in title.directors_summary:
        asc =  create_person_association(session,director,director_job)
        rec.persons.append(asc)

    #Writers
    writer_job,_= get_or_create(session,Job,description="Writer")
    for writer in title.directors_summary:
        asc =  create_person_association(session,writer,writer_job)
        rec.persons.append(asc)

    #Cast
    cast_job,_= get_or_create(session,Job,description="Cast")
    for cast in title.cast_summary:
        asc =  create_person_association(session,cast,cast_job)
        rec.persons.append(asc)


    return rec


def create_person_association(session,person,job):
    person,_ = get_or_create(session,Person,imdbid=person.imdb_id, name=person.name)
    asc = PersonM2M()
    asc.job = job
    asc.person= person
    return asc


def save_movie(*movies):
    engine = create_engine('sqlite:///test.db', echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    for movie in movies:
        try:
            rec = create_movie(session,movie)
            session.add(rec)
            session.commit()
            rec = create_movie(session,movie)
            session.add(rec)
            session.commit()
        except IntegrityError as e:
            logging.warning("Movie with imdbid:" + movie["imdbid"]+ " exists")
            session.rollback()
        except IsEpisode:
            logging.warning("Movie with imdbid:" + movie["imdbid"]+ " is classified as movie but it is episode")
            create_episode(session, movie)




def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True


"""-----------------------------Exceptions---------------------"""

class IsEpisode(Exception): pass
class IsMovie(Exception): pass


if __name__ == "__main__":
    pass


