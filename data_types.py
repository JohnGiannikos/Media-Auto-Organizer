__author__ = 'john'

from persistance import db_schema
from enum import Enum
from abc import ABC, abstractmethod

class DbObject(ABC):
    db_map = None

    def __init__(self):
        self.db_object = None

    @abstractmethod
    def create_db_object(self, db):pass

    @abstractmethod
    def load_from_db(self, db):pass

    @classmethod
    @abstractmethod
    def create_from_db(cls, db, db_obj):pass


class File(DbObject):
    db_map = db_schema.File

    def __init__(self, path=None, size=None, date_imported=None,media=None):
        super().__init__()
        self.path = path
        self.size = size
        self.media = media

    def create_db_object(self, db):
        media = self.media.create_db_object(db)

        self.db_object, _= db.get_or_create(self.db_map, path=self.path, size=self.size, media=media)

        return  self.db_object

    def load_from_db(self, db):
        obj = db.query(self.db_map, path=self.path)
        media = Media.create_from_db(obj.media)

        self.__init__(obj.path, obj.size, media)
        
        self.db_object = obj

    @classmethod
    def create_from_db(cls, db, db_obj):
        inst = cls(path = db_obj.path)
        inst.load_from_db(db)
        return inst


class Media(DbObject):
    db_map = db_schema.Media

    def __init__(self):
        super().__init__()
        self.genres = list()
        self.persons = list()

    def create_db_object(self, db):

        for genre in self.genres:
            new_genre = genre.create_db_object(db)
            self.db_object.genres.append(new_genre)

        for person in self.persons:
            new_person =  person.create_db_object(db)
            job = person.job.create_db_object(db)
            asc = db_schema.PersonM2M()
            asc.job = job
            asc.person = new_person
            self.db_object.persons.append(asc)

    def load_from_db(self, db):
        pass

    @classmethod
    def create_from_db(cls, db, db_obj):
        if type(db_obj) is db_schema.Episode:
            return Episode.create_from_db(db, db_obj)
        elif type(db_obj) is db_schema.Movie:
            return Movie.create_from_db(db, db_obj)

class Episode(Media):
    db_map = db_schema.Episode

    def __init__(self, imdbid=None, series=None, season=None, episode_no=None, tagline=None, title=None, rating=None,
                 year=None, runtime=None, release_date=None, plot_outline=None, cover_url=None, poster_url=None):
        super().__init__()
        self.imdbid = imdbid
        self.series = series
        self.season = season
        self.episode_no = episode_no
        self.tagline = tagline
        self.title = title
        self.rating = rating
        self.year = year
        self.runtime = runtime
        self.release_date = release_date
        self.plot_outline = plot_outline
        self.cover_url = cover_url
        self.poster_url = poster_url

    def create_db_object(self, db):

        new_series  = self.series.create_db_object(db)

        self.db_object,_ = db.get_or_create(self.db_map, imdbid=self.imdbid, series=new_series, season=self.season,
                                     episode_no=self.episode_no, tagline=self.tagline,title=self.title, rating=self.rating,
                                     year=self.year, runtime=self.runtime, release_date=self.release_date,
                                     plot_outline=self.plot_outline, cover_url=self.cover_url)

        super().create_db_object(db)

        return self.db_object

    def load_from_db(self, db):
        obj = db.query(self.db_map, imdbid=self.imdbid)
        if not obj:
            raise KeyError

        series =  Series.create_from_db(db, obj.series)
        self.__init__(obj.imdbid, series, obj.season, obj.episode_no, obj.tagline, obj.title, obj.rating, obj.year,
                      obj.runtime, obj.release_date, obj.plot_outline, obj.cover_url, obj.poster_url)

        for genre in obj.genres:
            new_genre = Genre.create_from_db(db, genre)
            self.genres.append(new_genre)

        for person in obj.persons:
            new_job = Job.create_from_db(db, person.job)
            new_person = Person.create_from_db(db, person.person)
            new_person.job = new_job
            self.persons.append(new_person)

        self.db_object = obj

    @classmethod
    def create_from_db(cls, db, db_obj):
        inst = cls(imdbid = db_obj.imdbid)
        inst.load_from_db(db)
        return inst

class Movie(Media):
    db_map = db_schema.Movie

    def __init__(self, imdbid=None, tagline=None, title=None, rating=None,year=None, runtime=None, release_date=None,
                 plot_outline=None, cover_url=None, poster_url=None):
        super().__init__()
        self.imdbid = imdbid
        self.tagline = tagline
        self.title = title
        self.rating = rating
        self.year = year
        self.runtime = runtime
        self.release_date = release_date
        self.plot_outline = plot_outline
        self.cover_url = cover_url

        self.poster_url = poster_url

    def create_db_object(self, db):


        self.db_object,_ = db.get_or_create(self.db_map, imdbid=self.imdbid, tagline=self.tagline,title=self.title,
                                     rating=self.rating, year=self.year, runtime=self.runtime,
                                     release_date=self.release_date, plot_outline=self.plot_outline, cover_url=self.cover_url)

        super().create_db_object(db)

        return self.db_object

    def load_from_db(self, db):
        obj = db.query(self.db_map, imdbid=self.imdbid)
        if not obj:
            raise KeyError

        self.__init__(obj.imdbid, obj.tagline, obj.title, obj.rating, obj.year, obj.runtime, obj.release_date,
                      obj.plot_outline, obj.cover_url, obj.poster_url)

        for genre in obj.genres:
            new_genre= Genre.create_from_db(db, genre)
            self.genres.append(new_genre)

        for person in obj.persons:
            new_job = Job.create_from_db(db, person.job)
            new_person = Person.create_from_db(db, person.person)
            new_person.job = new_job

        self.db_object = obj

    @classmethod
    def create_from_db(cls, db, db_obj):
        inst = cls(imdbid = db_obj.imdbid)
        inst.load_from_db(db)
        return inst

class Series(DbObject):

    db_map = db_schema.Series

    def __init__(self, imdbid=None, tagline=None, title=None, rating=None,year=None, plot_outline=None,
                 cover_url=None, poster_url=None):
        super().__init__()
        self.imdbid = imdbid
        self.tagline = tagline
        self.title = title
        self.rating = rating
        self.year = year
        self.plot_outline = plot_outline
        self.cover_url = cover_url
        self.poster_url = poster_url

    def create_db_object(self, db):
        self.db_object,_ = db.get_or_create(self.db_map, imdbid=self.imdbid, tagline=self.tagline,title=self.title,
                                     rating=self.rating, year=self.year, plot_outline=self.plot_outline, cover_url=self.cover_url)

        return self.db_object

    def load_from_db(self, db):
        obj = db.query(db_schema.Series, imdbid=self.imdbid)
        self.__init__(obj.imdbid, obj.tagline, obj.title, obj.rating,obj.year, obj.plot_outline, obj.cover_url,
                      obj.poster_url)

        self.db_object = obj

    @classmethod
    def create_from_db(cls, db, db_obj):
        inst = cls(imdbid = db_obj.imdbid)
        inst.load_from_db(db)
        return inst


class Genre(DbObject):
    db_map = db_schema.Genre

    def __init__(self, name=None):
        super().__init__()
        self.name = name

    def create_db_object(self, db):
        self.db_object = db.insert_obj(self.db_map, name=self.name)
        return self.db_object

    def load_from_db(self, db):
        obj = db.query(self.db_map, name=self.name)
        self.__init__( obj.name)

        self.db_object=obj

    @classmethod
    def create_from_db(cls, db, db_obj):
        inst = cls(name = db_obj.name)
        inst.load_from_db(db)
        return inst

class Person(DbObject):
    db_map = db_schema.Person

    def __init__(self, imdbid=None, name=None, job=None):
        super().__init__()
        self.imdbid = imdbid
        self.name = name
        self.job = job

    def create_db_object(self, db):
        self.db_object,_ = db.get_or_create(self.db_map, imdbid=self.imdbid, name=self.name)
        return self.db_object

    def load_from_db(self, db):
        obj = db.query(self.db_map, imdbid=self.imdbid)
        self.__init__(obj.imdbid, obj.name)

        self.db_object = obj

    @classmethod
    def create_from_db(cls, db, db_obj):
        inst = cls(imdbid = db_obj.imdbid)
        inst.load_from_db(db)
        return inst


class Job(DbObject):
    db_map = db_schema.Job

    def __init__(self, description=None):
        super().__init__()
        self.description = description

    def create_db_object(self, db):
        self.db_object = db.insert_obj(self.db_map, description=self.description)
        return self.db_object

    def load_from_db(self, db):
        obj = db.query(self.db_map, description=self.description)
        self.__init__(obj.description)

        self.db_object = obj

    @classmethod
    def create_from_db(cls, db, db_obj):
        inst = cls(description = db_obj.description)
        inst.load_from_db(db)
        return inst