__author__ = 'john'

import media_scanner
import persistence

import pickle

class Organizer ():


    def organize_folder(self,path):

        video =  media_scanner.scan_folder(path,1*8*1024*1024)

        video_with_data = media_scanner.get_movie_data(*video)

        return video_with_data

    def save(self,filename,data):
        with open(filename, 'wb') as handle:
            pickle.dump(data, handle)

    def load(self,filename):
        with open(filename, 'rb') as handle:
            return  pickle.load(handle)

if __name__ == "__main__":
    org = Organizer()
    #files = org.organize_folder("/home/john/test movies")
    files = org.load("sample.pickle")
    db = persistence.Database()
    db.save_movie(*files)



