# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go


import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


workbook_url = 'data//5-INTER.xlsx'


df = pd.read_excel(workbook_url, sheet_name = 'PASSES')

df['Team'] = df['Team'].fillna('Não identificado')
df['size'] = df["Passes per 90"]*df["Accurate passes, %"]/100


df = df.sort_values(by=['size'], ascending=False)

df['rank'] = df['size'].rank(method='first', ascending=False)

# separar dois conjuntos 
top_rank = 10
df_in = df[df["rank"] <= top_rank]
df_out = df[df["rank"] > top_rank]

x_text= "Passes per 90"
y_text= "Accurate passes, %"

hover = ("%%{text} [%%{customdata[0]}] <br><br>%s = %%{x}<br>%s = %%{y}<extra></extra>"% (x_text, y_text))



x_min=df[x_text].min()-5
x_max=df[x_text].max()+5

y_min=df[y_text].min()-5
y_max=df[y_text].max()+5


jumbotron = dbc.Jumbotron(
    [
        dbc.Container(
            [
                html.H1("Em busca de um craque", className="display-3"),
                html.P(
                    "Unimos o nosso gosto por futebol e dados. "
                    "Fizemos essa análise para ver quem poderia ser nosso próximo craque!",
                    className="lead",
                )
            ],
            fluid=True,
        )
    ],
    fluid=True,
)


app.layout = dbc.Container([
    jumbotron,
    
    html.Br(),
    dbc.InputGroup(
            [
                dbc.InputGroupAddon("Selecionar ranking", addon_type="prepend"),
                dbc.Input(id='my-input', value=10, type='number', min=1, max=len(df)),
            ],
            className="mb-3",
        ),
    html.Br(),
    dcc.Graph(id="scatter-plot",
              )
])



@app.callback(
    Output('scatter-plot', 'figure'),
    Input('my-input', 'value'))
def update_graph(ranking):
    top_rank = ranking
    df_in = df[df["rank"] <= top_rank]
    df_out = df[df["rank"] > top_rank]    
    
    fig = go.Figure()
    
    
    # conjunto do ranking
    for index, row in df_in.iterrows():
        fig.add_trace(go.Scattergl(
                x=[row['Passes per 90']], 
                y=[row['Accurate passes, %']], 
                mode='markers',
                text=[row['Player']],
                name=row['Player'],
                marker_size=20,
                hovertemplate=hover,
                customdata=[[row['Team']]],
                marker={'color': row['rank'],
                        'sizeref':.305,}))
    
        
    """    
    fig.add_trace(go.Scattergl(
                x=df_in['Passes per 90'], 
                y=df_in['Accurate passes, %'], 
                mode='markers',
                text=df_in['Player'],
                hovertemplate=hover,
                marker_size=df_in['size'],
                customdata=['Team', 'size'],
                marker={'color': df_in['rank'],
                        'size': df_in['size'],
                        'sizeref':2,}))
    """
    # conjunto fora do ranking
    for index, row in df_out.iterrows():
        fig.add_trace(go.Scattergl(
                x=[row['Passes per 90']], 
                y=[row['Accurate passes, %']], 
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
            x0=0, y0=df_in["Accurate passes, %"].mean(), x1=x_max, y1=df_in["Accurate passes, %"].mean(),     
            line=dict(color="gray",width=1.5, dash='dot'))
    
    fig.add_shape(type='line',
            x0=df_in["Passes per 90"].mean(), y0=0, x1=df_in["Passes per 90"].mean(), y1=y_max,     
            line=dict(color="gray",width=1.5, dash='dot'))

    return fig
    


if __name__ == '__main__':
    app.run_server(debug=True)