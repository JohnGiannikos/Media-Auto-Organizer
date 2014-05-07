__author__ = 'john'

from collections import defaultdict
from abc import ABC
import shutil

class Folder(defaultdict):
    def __init__(self, *args, **kwargs):
        super(Folder, self).__init__(Folder)



class Content(ABC):
    def __init__(self, path):
        self.path = path

class Link(Content):pass

class File(Content):

    def __init__(self, file):
        self.file = file
        self.path = file.path

    def move(self,new_path):
        shutil.move(self.path, new_path)
        self.file.path = new_path
        self.file._sa_instance_state.session.commit()


