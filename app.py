# -*- coding: utf-8 -*-

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go


from data import getData, getSheets, getXAxisText, getYAxisText
from layout import getLayout
from callbacks import getCallBacks

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
    
    x_text= getXAxisText(sheets[index])
    y_text= getYAxisText(sheets[index])
    
    hover = ("%%{text} [%%{customdata[0]}] <br><br>%s = %%{x}<br>%s = %%{y}<extra></extra>"% (x_text, y_text))
    
    x_min=df[x_text].min()-5
    x_max=df[x_text].max()+5
    
    y_min=df[y_text].min()-5
    y_max=df[y_text].max()+5
    
    
    # creat
    df_list.append(df)
    x_text_list.append(x_text)
    y_text_list.append(y_text)
    hover_list.append(hover)
    x_min_list.append(x_min)
    x_max_list.append(x_max)
    y_min_list.append(y_min)
    y_max_list.append(y_max)
    
    
    getCallBacks(app, df, 'scatter-plot-' + str(index+1), x_text, y_text, hover, x_min, x_max, y_min, y_max, sheets[index])






#getCallBacks(app, df, 'scatter-plot-2', x_text, y_text, hover, x_min, x_max, y_min, y_max)

    
"""
@app.callback(
    Output('scatter-plot-1', 'figure'),
    Input('my-input', 'value'))
def update_graph(ranking):
    
    top_rank = ranking
    df_in = df[df["rank"] <= top_rank]
    df_out = df[df["rank"] > top_rank]    
    
    fig = go.Figure()
    
    
    # conjunto do ranking
    for index, row in df_in.iterrows():
        fig.add_trace(go.Scattergl(
                x=[row[x_text]], 
                y=[row[y_text]], 
                mode='markers',
                text=[row['Player']],
                name=row['Player'],
                marker_size=20,
                hovertemplate=hover,
                customdata=[[row['Team']]],
                marker={'color': row['rank'],
                        'sizeref':.305,}))

    # conjunto fora do ranking
    for index, row in df_out.iterrows():
        fig.add_trace(go.Scattergl(
                x=[row[x_text]], 
                y=[row[y_text]], 
                mode='markers',
                text=[row['Player']],
                hovertemplate=hover,
                marker_size=10,
                customdata=[[row['Team']]],
                opacity=0.3,
                name=row['Player'], 
                marker={'sizemode':'area',
                        'sizeref':.305,
                        'color': 'gray'}))
    
    # Set axes ranges
    fig.update_xaxes(range=[x_min, x_max], title_text = x_text)
    fig.update_yaxes(range=[y_min, y_max], title_text = y_text)
    fig.update_layout(title_text='Passes', title_x=0.5)
    
    
    fig.add_shape(type='line',
            x0=0, y0=df_in[y_text].mean(), x1=x_max, y1=df_in[y_text].mean(),     
            line=dict(color="gray",width=1.5, dash='dot'))
    
    fig.add_shape(type='line',
            x0=df_in[x_text].mean(), y0=0, x1=df_in[x_text].mean(), y1=y_max,     
            line=dict(color="gray",width=1.5, dash='dot'))

    return fig
"""

if __name__ == '__main__':
    app.run_server(debug=True)