__author__ = 'john'

import os

from opensubtitles import OpenSubtitles
import imdbpie


def scan_folder(path,minSize=0):
    files = get_all_files_under_folder(path)

    filtered = [x["path"] for x in files if x["size"] >= minSize]

    with OpenSubtitles() as op:
        info = op.get_video_info(*filtered)

    return info


def get_all_files_under_folder(path):
    files_found = list()

    for root, subFolders, files in os.walk(path):
        if files:
            for file in files:
                full_path = os.path.join(root,file)
                rec = {"path" : full_path,
                       "size" : os.stat(full_path).st_size
                }
                files_found.append(rec)
    return files_found


def get_movie_data(*movies):
    data = list()
    imdb = imdbpie.Imdb()

    for movie in movies:
        all_data = imdb.find_movie_by_id(movie["imdbid"])
        movie["info"] = all_data
        data.append(movie)

    return data


if __name__ == "__main__":
    pass


