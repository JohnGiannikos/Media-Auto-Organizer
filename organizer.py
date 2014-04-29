__author__ = 'john'

import media_scanner
import persistence

import pickle

class Organizer ():

    def __init__(self):
        self.db = persistence.Database()

    def organize_folder(self,path):

        scanner = media_scanner.MediaScanner(self.db)
        scanner.scan_all_files_under_folder(path,1*8*1024*1024)
        scanner.filter_video()
        scanner.analyze_files()

    def save(self,filename,data):
        with open(filename, 'wb') as handle:
            pickle.dump(data, handle)

    def load(self,filename):
        with open(filename, 'rb') as handle:
            return  pickle.load(handle)

if __name__ == "__main__":

    org = Organizer()
    files = org.organize_folder("/home/john/test movies")
    #files = org.load("sample.pickle")
    #db = persistence.Database()
    #db.save_episodes(*files)



