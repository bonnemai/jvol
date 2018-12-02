import glob
import os
import logging

from jfile import JFile
logger=logging.getLogger(__name__)

def get_latest_file(pathname='./resources/J*'):
    list_of_files = glob.glob(pathname=pathname) # * means all if need specific format then *.csv
    if len(list_of_files)>0:
        latest_file = max(list_of_files, key=os.path.getctime)
        print (latest_file)
        return latest_file
    else:
        logging.warning('No file found in %s', pathname)


today_file=JFile()
# TODO: Use holidays to get T-1 file and keep the path of the file somewhere.
yesterday_file=JFile(is_today=False)
index_name='NKY'
if today_file is None:
    logger.warning('No File for today, please contact J')
else:
    # Today tests
    today_spot=today_file.get_spot(index_name=index_name)
    today_atm_vol=today_file.get_vol_value(moneyness='percent', strike=100, expiry='7Dec18', index_name=index_name)
    if today_atm_vol is None:
        logger.warning('No ATMVol for today, please contact J')
    elif today_spot is None:
        logger.warning('No Spot for today, please contact J')

    # Today vs T-1 tests
    yesterday_spot=yesterday_file.get_spot(index_name=index_name)
    yesterday_atm_vol=yesterday_file.get_vol_value(moneyness='percent', strike=100, expiry='7Dec18', index_name=index_name)

    if today_spot==yesterday_spot:
        logger.warning('Today Spot is the same as t-1 (%s) for %s', yesterday_file.path, index_name)
    if today_atm_vol==yesterday_atm_vol:
        logger.warning('Today ATM Vol is the same as t-1 (%s) for %s', yesterday_file.path, index_name)