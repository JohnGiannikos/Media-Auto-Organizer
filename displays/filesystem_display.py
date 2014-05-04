__author__ = 'john'

from views.tree import *
import os.path
import os

class FilesystemDisplay():

    def __init__(self, path):
        self.path = path


    def apply_view(self, view):
        self.recursive_traverse(self.path, view.root)


    def recursive_traverse(self, path, parent):
        for  key,value in parent.items():
            new_path = os.path.join(path, key)
            self.make_dir(new_path)
            print(new_path)
            if type(value) is Folder:
                self.recursive_traverse(new_path, value)
            else:
                self.create_record(new_path, value)

    def make_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def create_record(self, path, media):

        os.symlink(media['link'], os.path.join(path, os.path.basename(media['link']) ))




