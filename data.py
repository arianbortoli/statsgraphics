# -*- coding: utf-8 -*-

import pandas as pd

# file path of our main excel
workbook_url = 'data//5-INTER.xlsx'

# return all sheets from our main excel 
def getSheets():

    all_dfs = pd.read_excel(workbook_url, sheet_name=None)
    
    return list(all_dfs.keys())


# return dataframe 
def getData(sheet):
    
    df = pd.read_excel(workbook_url, sheet_name = sheet)
    
    df['Team'] = df['Team'].fillna('Não identificado')
    col_2 = df.columns[2]
    col_3 = df.columns[3]
    
    df['size'] = df[col_2]*df[col_3]/100
    
    
    df = df.sort_values(by=['size'], ascending=False)
    
    df['rank'] = df['size'].rank(method='first', ascending=False)
    
    return df


def getXAxisText(sheet):
    
    df = pd.read_excel(workbook_url, sheet_name = sheet)

    return (df.columns[2])


def getYAxisText(sheet):
    
    df = pd.read_excel(workbook_url, sheet_name = sheet)

    return (df.columns[3])