# import xlrd
# from JException import JException
from xlrd import open_workbook
import logging

logger=logging.getLogger(__name__)

def has_cell(index_sheet, i, j):
    try:
        return index_sheet.cell_value(i, j)!=''
    except:
        return False


class JException(Exception):
    def __init__(self, message):
        super().__init__(message)


class JFile():
    def __init__(self, is_today=True, region='APAC', date_str=None, path=r'./resources/J_Vol.xlsx', indices=['NKY', 'KOSPI2', 'HSCEI', 'HSI']):
        if path is None:
            if region=='DEV':
                self.path=r'./test/resources/J_Vol.xlsx'
        else:
            self.path=path
        self.results={}
        self.comments=[]
        # TODO: find files, get the latest, add a comment...

        workbook=open_workbook(path)
        logger.info('Sheets found: %s', workbook.sheet_names())
        for index_name in indices:
            index_sheet=workbook.sheet_by_name(index_name)
            spot=index_sheet.cell(1, 2).value
            if spot is None or spot==0:
                raise JException('No Spot found for %s'.format(index_name))

            i_strike=2
            i_abs_expiries=3
            abs_strikes=[]
            abs_expiries=[]
            rel_strikes=[]
            rel_expiries=[]
            abs_vol_surface=[]
            while index_sheet.cell_value( 2, i_strike)!='':
                abs_strikes.append(index_sheet.cell_value( 2, i_strike))
                i_strike+=1
            while index_sheet.cell_value( i_abs_expiries,0 )!='':
                abs_expiries.append(index_sheet.cell_value( i_abs_expiries, 0))
                vol_line=[]
                for i in range(1,i_strike):
                    vol_line.append(index_sheet.cell_value(i_abs_expiries, i))
                i_abs_expiries+=1
                abs_vol_surface.append(vol_line)

            i_strike=2
            i_abs_expiries+=1
            rel_vol_surface=[]
            while index_sheet.cell_value( i_abs_expiries, i_strike)!='':
                rel_strikes.append(index_sheet.cell_value( i_abs_expiries, i_strike))
                i_strike+=1
            i_abs_expiries+=1
            while has_cell( index_sheet, i_abs_expiries,0 ):
                rel_expiries.append(index_sheet.cell_value( i_abs_expiries, 0))
                vol_line=[]
                for i in range(1,i_strike):
                    vol_line.append(index_sheet.cell_value(i_abs_expiries, i))
                rel_vol_surface.append(vol_line)
                i_abs_expiries+=1

            self.results[index_name]={'spot': spot,
                                      'absolute': {'strikes': abs_strikes,
                                      'expiries': abs_expiries,
                                      'vol_surface':abs_vol_surface},
                                      'relative': {'strikes': rel_strikes,
                                      'expiries': rel_expiries,
                                      'vol_surface':rel_vol_surface}}

    def get_vol_value(self, strike, expiry, moneyness='absolute', index_name='NKY'):
        vol_surface=self.results[index_name][moneyness]
        i_expiry=vol_surface['expiries'].index(expiry)
        i_strike=vol_surface['strikes'].index(strike)
        return vol_surface['vol_surface'][i_expiry][i_strike]

    def get_spot(self, index_name='NKY'):
        return self.results[index_name]['spot']

    def add_comment(self, comment, criticity='info'):
        self.comments.append({'comment': comment, criticity:criticity})

