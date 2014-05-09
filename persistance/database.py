__author__ = 'john'
import logging

from persistance.db_schema import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy.exc import IntegrityError, OperationalError
import os
import time

class Database():
    def __init__(self, path):
        self.engine = create_engine('sqlite:///'+ os.path.join(path,'organizer.db'), echo=True)
        #Base.metadata.drop_all(self.engine)
        #Base.metadata.create_all(self.engine)
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session(autocommit=False)

    def find_files(self,**kwargs):
        return self.session.query(File).filter_by(**kwargs).all()

    def save_file(self,file):
        try:
            self.session.add(file)
            self.commit()
        except IntegrityError as e:
            self.session.rollback()
            logging.error("Error inserting file %s" % str(e))

    def insert_obj(self,type, **kwargs):
        obj,_ = self.get_or_create(type, **kwargs)
        self.session.add(obj)
        self.commit()
        return obj

    def commit(self):
        for i in range(5):
            try:
                self.session.commit()
                return
            except OperationalError:
                logging.error('Database is locked, waiting 3 seconds')
                time.sleep(3)


    def query(self, model, **kwargs):
        return self.session.query(model).filter_by(**kwargs).first()

    def get_or_create(self, model, defaults=None, **kwargs):
        instance = self.session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance, False
        else:
            params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
            params.update(defaults or {})
            instance = model(**params)
            return instance, True


if __name__ == "__main__":
    pass


