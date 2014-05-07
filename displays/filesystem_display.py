__author__ = 'john'

import views
from views.categories import *
import os
import shutil

class FilesystemDisplay():

    def __init__(self, path):

        if not os.path.exists(path):
            os.makedirs(path)

        self.path = path


    def apply_view(self, view):
        self.create_tree(self.path, view.root)
        self.clean_tree(self.path, view.root)


    def create_tree(self, path, parent):
        for key,value in parent.items():
            new_path = os.path.join(path, key)
            self.make_dir(new_path)
            if type(value) is views.Folder:
                self.create_tree(new_path, value)
            else:
                try:
                    self.create_record(new_path, value)
                except FileExistsError:
                    continue

    def clean_tree(self, path, parent):

        folders = os.listdir(path)

        for folder in folders :
            if folder not in parent.keys():
                shutil.rmtree(os.path.join(path, folder))

        for key,value in parent.items():
            new_path = os.path.join(path, key)
            self.make_dir(new_path)
            if type(value) is  views.Folder:
                self.clean_tree(new_path, value)


    def make_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def create_record(self, path, contents):
        for content in contents:
            final_path = os.path.join(path, os.path.basename(content.path))
            if type(content) is views.Link:
                os.symlink(content.path, final_path)
            if type(content) is views.File:
                if os.path.split(content.path) != final_path:
                    content.move(final_path)





