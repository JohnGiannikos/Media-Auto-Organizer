__author__ = 'john'


from sqlalchemy import Column, Integer, String , Float, Date, ForeignKey
from sqlalchemy.orm import relationship, backref

from sqlalchemy.ext.declarative import declarative_base



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
    poster_url = Column(String)

class Series(Base):
    __tablename__ = 'series'
    id = Column(Integer, primary_key=True)
    imdbid = Column(String, unique=True)
    title = Column(String)
    year = Column(Integer)
    image_url = Column(String)
    episodes = relationship("Episode",backref="series")

class Episode(File):
    __tablename__ = 'episodes'
    __mapper_args__ = {'polymorphic_identity': 2}
    episode_id = Column('id',Integer,ForeignKey('files.id'), primary_key=True)
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
