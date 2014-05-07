from persistance import database

__author__ = 'john'

import media_scanner
import os
import logging
from views.categories import CategoriesTree
from displays.filesystem_display import FilesystemDisplay
from views.storage import StorageView
import persistance.db_schema as db_schema


class Organizer ():

    def __init__(self):
        self.db = database.Database()
        self.config = dict()
        exec(open("setting.conf").read(), self.config)

        self.filemanager = StorageView(self.db)
        self.scan_paths()


    def scan_paths(self):

        scanner = media_scanner.MediaScanner(self.db)

        for path in self.config['media_paths']:
            if os.path.isdir(path):
                scanner.scan_all_files_under_folder(path,1*8*1024*1024)
            else:
                logging.error("Not valid media path : %s" % path)

        scanner.filter_video()
        scanner.filter_old()
        scanner.analyze_files()
        fs = CategoriesTree(self.db)
        fs.create_view()
        dis = FilesystemDisplay('/home/john/test tree')
        dis.apply_view(fs)


        self.filemanager.create_view()
        dis = FilesystemDisplay('/home/john/testraw')
        dis.apply_view(self.filemanager)






if __name__ == "__main__":

    org = Organizer()



