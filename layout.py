# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


jumbotron = dbc.Jumbotron(
    [
        dbc.Container(
            [
                html.H1("Em busca de um craque", className="display-3"),
                html.P(
                    "Unimos a nossa paixão por futebol e análise de dados para fazer essa pesquisa. ",
                    className="lead",
                ),
                html.Hr(className="my-2"),
                html.P(
                    "Nosso objetivo é encontrar quem poderia ser nosso próximo craque!",
                ),
            ],
        )
    ],
)


def getLayout(app, max_size):
    app.layout = dbc.Container([
        (jumbotron),



        html.Div([html.P('Primeiro pegamos os dados em: '), html.A("#")]),




        html.Div(
            [
                dbc.InputGroup(
                    [
                        dbc.InputGroupAddon(
                            "Selecionar ranking", addon_type="prepend"),
                        dbc.Input(id='my-input', value=10,
                                  type='number', min=1, max=max_size),

                    ],
                    className="mb-3",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupAddon(
                            dbc.Checkbox(id="checkbox", checked=True), addon_type="prepend"),


                        dbc.InputGroupAddon(
                            "Mostrar jogadores fora do ranking", addon_type="append"),
                    ],
                    className="mb-3",
                )
            ]
        ),


        html.Br(),
        dcc.Graph(id="scatter-plot-1"),
        dcc.Graph(id="scatter-plot-2"),
        dcc.Graph(id="scatter-plot-3"),
        dcc.Graph(id="scatter-plot-4"),
        dcc.Graph(id="scatter-plot-5"),
        dcc.Graph(id="scatter-plot-6"),

        html.Br(),
        html.Div(id='Table',
                 style={'width': '100%',
                        'height': '750px',
                        'overflow-y': 'scroll',
                        'padding': '10px 10px 10px 20px'
                        },)

    ], fluid=True)

    return app
