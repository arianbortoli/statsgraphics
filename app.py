# -*- coding: utf-8 -*-

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd


from data import getData, getSheets, getXAxisText, getYAxisText
from layout import getLayout
from callbacks import getCallBacks, getTableCallBack

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

df = getData('PASSES')

sheets = getSheets()

df_list = list()
x_text_list = list()
y_text_list = list()
hover_list = list()
x_min_list = list()
x_max_list = list()
y_min_list = list()
y_max_list = list()

app = getLayout(app, len(df))


for index in range(6):
    df = getData(sheets[index])

    x_text = getXAxisText(sheets[index])
    y_text = getYAxisText(sheets[index])

    hover = (
        "%%{text} [%%{customdata[0]}] <br><br>%s = %%{x}<br>%s = %%{y}<extra></extra>" % (x_text, y_text))

    x_min = df[x_text].min()-5
    x_max = df[x_text].max()+5

    y_min = df[y_text].min()-5
    y_max = df[y_text].max()+5

    # creat
    df_list.append(df)
    x_text_list.append(x_text)
    y_text_list.append(y_text)
    hover_list.append(hover)
    x_min_list.append(x_min)
    x_max_list.append(x_max)
    y_min_list.append(y_min)
    y_max_list.append(y_max)

    getCallBacks(app, df, 'scatter-plot-' + str(index+1), x_text,
                 y_text, hover, x_min, x_max, y_min, y_max, sheets[index])


getTableCallBack(app, df_list[0], 'Table')

if __name__ == '__main__':
    app.run_server(debug=True)
