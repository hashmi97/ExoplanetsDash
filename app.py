# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from utils import *
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output


app = Dash(__name__)

fig1 = generate_plot(DEFAULT_PLANET_1)
fig2 = generate_plot(DEFAULT_PLANET_2)
app.layout = html.Div(
    children=[
        html.H1(
            children=
            'Exoplanet Dashboard',
            style={'textAlign': 'center'}
        ),

        html.Div(
            children=[
                '''
                    ExopD: A web application to visualize exoplanets data.
                ''',
                html.Hr()],
            style={'textAlign': 'center'}
        ),
        html.Div( # Dropdown
            children=[
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id='planet1-name',
                            options=[{'label': i, 'value': i} for i in available_planets],
                            clearable=False,
                            placeholder="Select a Planet"

                        )
                    ],
                    style={'width': '49%', 'display': 'inline-block', 'border-right': '1px solid black',
                           'border-right-style': 'dashed'}
                ),
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id='planet2-name',
                            options=[{'label': i, 'value': i} for i in available_planets],
                            clearable=False,
                            placeholder="Select a Planet"
                        )
                    ],
                    style={'width': '49%', 'display': 'inline-block', 'border-left': '1px solid black',
                           'border-left-style': 'dashed'}
                )
            ],
        ),

        html.Div( # Figures
            children=[
                dcc.Graph(
                    id='planet1-fig',
                    figure=fig1,
                    style={'width': '49%', 'display': 'inline-block', 'border-right': '1px solid black',
                           'border-right-style': 'dashed'}
                ),
                dcc.Graph(
                    id='planet2-fig',
                    figure=fig2,
                    style={'width': '49%', 'display': 'inline-block', 'border-left': '1px solid black',
                           'border-left-style': 'dashed'}
                )]),

        html.Div( # Tables
            children=[
                html.Div(
                    children=[
                        dash_table.DataTable(
                            id='planet1-table',
                            data=getPlanetTableDF(DEFAULT_PLANET_1).to_dict('records'),
                            columns=[{'id': c, 'name': c} for c in getPlanetTableDF('Earth').columns],
                            style_cell={'textAlign': 'center'},
                            style_data={
                                'color': 'black',
                                'backgroundColor': 'white'
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(220, 220, 220)',
                                }
                            ],
                            style_header={
                                'backgroundColor': 'rgb(210, 210, 210)',
                                'color': 'black',
                                'fontWeight': 'bold'
                            }
                        )
                    ],
                    style={'width': '49%', 'display': 'inline-block', 'border-right': '1px solid black',
                           'border-right-style': 'dashed'}
                ),

                html.Div(
                    children=[
                        dash_table.DataTable(
                            id='planet2-table',
                            data=getPlanetTableDF(DEFAULT_PLANET_2).to_dict('records'),
                            columns=[{'id': c, 'name': c} for c in getPlanetTableDF('HD 80606 b').columns],
                            style_cell={'textAlign': 'center'},
                            style_data={
                                'color': 'black',
                                'backgroundColor': 'white'
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(220, 220, 220)',
                                }
                            ],
                            style_header={
                                'backgroundColor': 'rgb(210, 210, 210)',
                                'color': 'black',
                                'fontWeight': 'bold'
                            }
                        )
                    ],
                    style={'width': '49%', 'display': 'inline-block', 'border-left': '1px solid black',
                           'border-left-style': 'dashed'}
                ),
            ]
        ),

        html.Div( # Text later
            children=[
                html.Hr(),
                dcc.Markdown(ADDENDUM,
                             style={"white-space": "pre"}),
                html.Hr()],
            style={'width': '100%', 'justify-content': 'center',
                   'textAlign': 'center'
                   }

        ),
        html.Div(
            children=[
                'Copyright (C) 2022 Hisham Al Hashmi',
                html.A(
                    'Github repo',
                    href='https://github.com/hashmi97/ExoplanetsDash',
                    target='_blank',
                    style={'margin-left': '15px', 'margin-right': '15px'}
                ),
            ],
            style={'width': '100%', 'display': 'flex',  'align-items': 'center', 'justify-content': 'center',
                   'textAlign': 'center'
                   }
        ),
        html.Div(
            'This data was gathered from the NASA Exoplanet Archive. This was done by the California Institute of Technology, under contract with the National Aeronautics and Space Administration under the Exoplanet Exploration Program',
            style={'width': '100%', 'display': 'flex',  'align-items': 'center', 'justify-content': 'center',
                   'textAlign': 'center'
                   }
        )

    ]
)


@app.callback(
    Output('planet1-fig', 'figure'),
    Output('planet2-fig', 'figure'),
    Output('planet1-table', 'data'),
    Output('planet2-table', 'data'),
    Input('planet1-name', 'value'),
    Input('planet2-name', 'value'))
def update_figure(planet1_name, planet2_name):
    if planet1_name is None:
        planet1_name = DEFAULT_PLANET_1
    if planet2_name is None:
        planet2_name = DEFAULT_PLANET_2
    planet1_fig = generate_plot(planet1_name)
    planet2_fig = generate_plot(planet2_name)
    planet1_df = getPlanetTableDF(planet1_name)
    planet2_df = getPlanetTableDF(planet2_name)

    return planet1_fig, planet2_fig, planet1_df.to_dict('records'), planet2_df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
