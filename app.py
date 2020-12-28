import dash
import dash_core_components as dcc
import dash_html_components as html
#from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


workbook_url = 'data//5-INTER.xlsx'

df = pd.read_excel(workbook_url, sheet_name = 'PASSES')

df['Team'] = df['Team'].fillna('Não identificado')
df['size'] = df["Passes per 90"]*df["Accurate passes, %"]/100

fig = px.scatter(
        df, x="Passes per 90", y="Accurate passes, %", color="Team", size='size', 
        hover_data=['Player'])

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Análises"),
    dcc.Graph(id="scatter-plot",
              figure = fig)
])

app.run_server(debug=False)