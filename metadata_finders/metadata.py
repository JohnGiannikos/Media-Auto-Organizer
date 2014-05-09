__author__ = 'john'

from abc import ABC, abstractmethod


class Metadata(ABC):

    def __init__(self, db):
        self.db = db

    @abstractmethod
    def update_metadata(self, *files): pass

