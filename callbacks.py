# -*- coding: utf-8 -*-

from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


def getCallBacks(app, df, graph_id, x_text, y_text, hover, x_min, x_max, y_min, y_max, title):
    @app.callback(
        Output(graph_id, 'figure'),
        [
            Input('my-input', 'value'),
            Input('checkbox', 'checked')
        ],)
    def update_graph(ranking, checkbox_checked):

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
                        'sizeref': .305, }))

        # conjunto fora do ranking
        if checkbox_checked:

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
                    marker={'sizemode': 'area',
                            'sizeref': .305,
                            'color': 'gray'}))

        # Set axes ranges
        fig.update_xaxes(range=[x_min, x_max], title_text=x_text)
        fig.update_yaxes(range=[y_min, y_max], title_text=y_text)
        fig.update_layout(title_text=title, title_x=0.5)

        fig.add_shape(type='line',
                      x0=0, y0=df_in[y_text].mean(), x1=x_max, y1=df_in[y_text].mean(),
                      line=dict(color="gray", width=1.5, dash='dot'))

        fig.add_shape(type='line',
                      x0=df_in[x_text].mean(), y0=0, x1=df_in[x_text].mean(), y1=y_max,
                      line=dict(color="gray", width=1.5, dash='dot'))

        return fig


def getTableCallBack(app, df, table_id):

    @ app.callback(
        Output(table_id, 'children'),
        Input('my-input', 'value'))
    def update_table(Ranking):
        table = dbc.Table.from_dataframe(
            df, striped=True, bordered=True, hover=True, responsive=True)

        return table
        """ 
        return dbc.Table.from_dataframe(df,
                                        bordered=True,
                                        dark=True,
                                        hover=True,
                                        responsive=True,
                                        striped=True,)
        """
