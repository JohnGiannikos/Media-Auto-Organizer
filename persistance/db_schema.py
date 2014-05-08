__author__ = 'john'


from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

Base = declarative_base()


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    media_id = Column(Integer, ForeignKey('media.id'))
    path = Column(String, unique=True)
    size = Column(Integer)
    date_imported = Column(DateTime, default=datetime.now)
    media = relationship('Media', backref="files")


genre_association_table = Table('genre_m2m', Base.metadata,
    Column('media_id', Integer, ForeignKey('media.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)

class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    type = Column("type", Integer)
    genres = relationship("Genre", secondary=genre_association_table, backref="media")
    persons = relationship("PersonM2M", backref="media")

    __mapper_args__ = {'polymorphic_on': type}


class Movie(Media):
    __tablename__ = 'movies'
    __mapper_args__ = {'polymorphic_identity': 1}
    movie_id = Column('id',Integer,ForeignKey('media.id'), primary_key=True)
    imdbid = Column(String, unique=True,primary_key=True)
    tagline = Column(String)
    title = Column(String)
    rating = Column(Float)
    year = Column(Integer)
    runtime = Column(String)
    release_date = Column(Date)
    plot_outline = Column(String)
    cover_url = Column(String)
    poster_url = Column(String)


class Series(Base):
    __tablename__ = 'series'
    id = Column(Integer, primary_key=True)
    imdbid = Column(String, unique=True)
    tagline = Column(String)
    title = Column(String)
    rating = Column(Float)
    year = Column(Integer)
    plot_outline = Column(String)
    cover_url = Column(String)
    poster_url = Column(String)
    episodes = relationship("Episode",backref="series")


class Episode(Media):
    __tablename__ = 'episodes'
    __mapper_args__ = {'polymorphic_identity': 2}
    episode_id = Column('id',Integer,ForeignKey('media.id'), primary_key=True)
    imdbid = Column(String, unique=True,primary_key=True)
    series_id = Column(Integer,ForeignKey('series.id'))
    season = Column(Integer)
    episode_no = Column(Integer)
    tagline = Column(String)
    title = Column(String)
    rating = Column(Float)
    year = Column(Integer)
    runtime = Column(String)
    release_date = Column(Date)
    plot_outline = Column(String)
    cover_url = Column(String)
    poster_url = Column(String)


class Genre(Base):
    __tablename__= 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer,primary_key=True)
    imdbid = Column(String, unique=True)
    name = Column(String)


class PersonM2M(Base):
    __tablename__='person_m2m'
    id = Column(Integer,primary_key=True)
    media_id = Column(Integer, ForeignKey('media.id'))
    person_id = Column(Integer, ForeignKey('persons.id'))
    job_id = Column(Integer,ForeignKey('jobs.id'))
    job = relationship('Job')
    person = relationship("Person", backref="media_assocs")


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer,primary_key=True)
    description = Column(String)
