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

    df = pd.read_excel(workbook_url, sheet_name=sheet)

    df['Team'] = df['Team'].fillna('Não identificado')
    col_2 = df.columns[2]
    col_3 = df.columns[3]

    df['size'] = df[col_2]*df[col_3]/100

    df = df.sort_values(by=['size'], ascending=False)

    df['rank'] = df['size'].rank(method='first', ascending=False)

    df['new_index'] = df['Player']
    df = df.set_index("new_index")
    return df


def getXAxisText(sheet):

    df = pd.read_excel(workbook_url, sheet_name=sheet)

    return (df.columns[2])


def getYAxisText(sheet):

    df = pd.read_excel(workbook_url, sheet_name=sheet)

    return (df.columns[3])


def getFullDf():
    sheets = getSheets()
    fullDF = pd.DataFrame()

    for i in range(len(sheets)-1):
        aux_df = getData(sheets[i])

        if len(fullDF.index) == 0:
            col_2 = aux_df.columns[2]
            col_3 = aux_df.columns[3]
            fullDF = aux_df[["Player", "Team", col_2, col_3, 'size']]
        else:
            col_2 = aux_df.columns[2]
            col_3 = aux_df.columns[3]
            aux_df = aux_df[["Player", "Team", col_2, col_3, 'size']]
            aux_df.rename(columns={'size': 'size_'+str(i)}, inplace=True)

            fullDF = pd.merge(fullDF, aux_df, how="left",
                              left_index=True, right_index=True, suffixes=('', '_y'))

            fullDF.drop(fullDF.filter(regex='_y$').columns.tolist(),
                        axis=1, inplace=True)

    fullDF = fullDF.drop_duplicates(keep='first')
    fullDF['sizeTotal'] = fullDF[['size', 'size_1', 'size_2',
                                  'size_3', 'size_4', 'size_5']].sum(axis=1)

    fullDF['rank'] = fullDF['sizeTotal'].rank(method='first', ascending=False)

    fullDF = fullDF.drop(['size', 'size_1', 'size_2',
                          'size_3', 'size_4', 'size_5', 'sizeTotal'], axis=1)

    fullDF.sort_values('rank', inplace=True)
    return fullDF
