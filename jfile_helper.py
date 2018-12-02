import glob
import os
import logging


def get_latest_file(pathname='./resources/*'):
    list_of_files = glob.glob(pathname=pathname) # * means all if need specific format then *.csv
    if len(list_of_files)>0:
        latest_file = max(list_of_files, key=os.path.getctime)
        print (latest_file)
        return latest_file
    else:
        logging.warning('No file found')