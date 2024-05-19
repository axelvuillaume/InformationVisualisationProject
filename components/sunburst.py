from dash import dcc, html, Input, Output, callback

import plotly.express as px
from utils.load_data import cleaned_games, categories

def graph_sunburst():
    return html.Div([
    dcc.Checklist(
        id='hide_single_player',
        options=[
            {'label': 'Hide Single-player', 'value': 'Single-player'}
        ],
        value=[],  # Balue default : no
        style={ 
            'color': 'white' 
        }
    ),
    dcc.Graph(id='sunburst_graph'),
    dcc.Slider(
        id='seuil_slider',
        min=0,
        max=50000,
        step=1000,
        value=20000,
        marks={i: str(i) for i in range(0, 50001, 10000)}
    ),
    html.Div(id='slider_output',         style={ 
            'color': 'white' 
        })
])

@callback(Output('sunburst_graph', 'figure'),
          [Input('hide_single_player', 'value'),
           Input('seuil_slider', 'value')
          ])
def update_graph(hide_single_player, seuil_minimum):
    merged_data = cleaned_games.merge(categories, on='app_id', how='inner')
    if 'Single-player' in hide_single_player:
        merged_data_grouped = merged_data.groupby('name').first().reset_index()
        merged_data_grouped = merged_data_grouped.drop(merged_data_grouped[merged_data_grouped['categories'] == 'Single-player'].index)
    else:
        merged_data_grouped = merged_data.groupby('name').first().reset_index()

    merged_data_filtered = merged_data_grouped[merged_data_grouped['average_playtime_forever'] >= seuil_minimum]
    
    fig = px.sunburst(
        merged_data_filtered,
        path=['categories', 'developers', 'name'],
        values='average_playtime_forever',
    )

    return fig

@callback(Output('slider_output', 'children'),
          [Input('seuil_slider', 'value')]
         )
def update_slider_output(seuil_minimum):
    return f'Seuil minimum : {seuil_minimum}'
