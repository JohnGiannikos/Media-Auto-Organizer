from persistance import database

__author__ = 'john'

import media_scanner


class Organizer ():

    def __init__(self):
        self.db = database.Database()

    def organize_folder(self,path):

        scanner = media_scanner.MediaScanner(self.db)
        scanner.scan_all_files_under_folder(path,1*8*1024*1024)
        scanner.filter_video()
        scanner.filter_old()
        scanner.analyze_files()


if __name__ == "__main__":

    org = Organizer()
    #files = org.organize_folder("/home/john/mount/samba/DATA-SERVER/Data/Torrents/Completed")
    files = org.organize_folder("/home/john/test movies")
    #files = org.load("sample.pickle")
    #db = persistence.Database()
    #db.save_episodes(*files)



