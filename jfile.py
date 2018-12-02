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
    def __init__(self, is_today=True, region='APAC', date_str=None, path=r'./resources/J_Vol.xlsx'):
        if path is None:
            if region=='DEV':
                path=r'./test/resources/J_Vol.xlsx'
        self.results={}
        self.comments=[]
        # TODO: find files, get the latest, add a comment...
        index_name="NKY"
        workbook=open_workbook(path)
        print(workbook.sheet_names())
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
        # i_rel_expiries=1
        rel_vol_surface=[]
        while index_sheet.cell_value( i_abs_expiries, i_strike)!='':
            rel_strikes.append(index_sheet.cell_value( i_abs_expiries, i_strike))
            i_strike+=1
        i_abs_expiries+=1
        while has_cell( index_sheet, i_abs_expiries,0 ):
            rel_expiries.append(index_sheet.cell_value( i_abs_expiries, 0))
            vol_line=[]
            # if has_cell( index_sheet, i_abs_expiries,0 ):
            for i in range(1,i_strike):
                vol_line.append(index_sheet.cell_value(i_abs_expiries, i))
            rel_vol_surface.append(vol_line)
            i_abs_expiries+=1

        self.results[index_name]={'spot': spot,
                                  'abs_strikes': abs_strikes,
                                  'abs_expiries': abs_expiries,
                                  'abs_vol_surface':abs_vol_surface,
                                  'rel_strikes': rel_strikes,
                                  'rel_expiries': rel_expiries,
                                  'rel_vol_surface':rel_vol_surface}


    def add_comment(self, comment, criticity='info'):
        # print(self.comments.a)
        self.comments.append({'comment': comment, criticity:criticity})

