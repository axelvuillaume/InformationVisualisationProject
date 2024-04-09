from dash import dcc
from dash import html
from utils.data_processing import get_game_list_from_api
from utils.data_processing import get_n_best_gen_or_cat
from utils.data_processing import get_n_best_gen_or_cat_by_hours
import plotly.graph_objs as go
import numpy as np
import random

def hexagon(categories, genres, n):

    games = get_game_list_from_api(76561198150561997)
    select = 'genres' 

    if(select == 'genres'):
        ranking = get_n_best_gen_or_cat_by_hours(games, genres, n)
    if(select == 'categories'):
        ranking = get_n_best_gen_or_cat_by_hours(games, categories, n)

    print(ranking)

    ranking_pairs = list(ranking.items())
    random.shuffle(ranking_pairs)
    ranking = dict(ranking_pairs)

    max_value = max(ranking.values())
    normalized_values = [value / max_value for value in ranking.values()]

    polygon_back = get_polygon(n, [1] * n, 'blue', 0.1)
    text_trace = add_text_labels(list(ranking.keys()))
    polygon_top = get_polygon(n, normalized_values, 'blue', 1)
    lines = get_middle_lines(n, [1] * n)

    # Create the layout for the graph
    layout = go.Layout(
        xaxis=dict(visible=False, range=[-1.5, 1.5]),  # Hide x-axis
        yaxis=dict(visible=False, range=[-1.5, 1.5]),  # Hide y-axis
        showlegend=False,  # Hide legend
        width=500,  # Set width of the graph
        height=500,  # Set height of the graph
        margin=dict(l=1, r=1, t=1, b=1),
        dragmode='select',  # Disable zoom and pan
    )

    # Create the figure containing the trace and layout
    fig = go.Figure(data=[polygon_back, polygon_top, text_trace] + lines , layout=layout)

    # Return the Dash component with the graph
    return dcc.Graph(id='hexagone-component',figure=fig)

def get_polygon_coords(n, center_distances):
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    vertices_x = [distance * np.cos(angle) for distance, angle in zip(center_distances, angles)]
    vertices_y = [distance * np.sin(angle) for distance, angle in zip(center_distances, angles)]
    return vertices_x, vertices_y

def get_polygon(n, center_distances, color, opacity):
    x, y = get_polygon_coords(n, center_distances)
    # Create a Scatter trace for the polygon
    polygon_trace = go.Scatter(
        x=x + [x[0]],  # Close the polygon by repeating the first vertex
        y=y + [y[0]],
        mode='lines',  # Draw lines to connect vertices
        line=dict(color=color),  # Set line color
        fill='toself',  # Fill the area inside the polygon
        fillcolor=f'rgba(0, 0, 255, {opacity})'  # Set fill color with opacity
    )
    return polygon_trace

def get_middle_lines(n, center_distances,  color='white'):
    x, y = get_polygon_coords(n, center_distances)
    center_x = 0
    center_y = 0
    
    # Create line traces from center to each vertex
    line_traces = []
    for i in range(n):
        line_trace = go.Scatter(
            x=[center_x, x[i]],
            y=[center_y, y[i]],
            mode='lines',
            line=dict(color=color, width=1)
        )
        line_traces.append(line_trace)
    
    return line_traces

def add_text_labels(labels):
    x, y = get_polygon_coords(len(labels), [1] * len(labels))
    #multiply all x and y by 1.1 to make the text appear outside the polygon
    x = [i * 1.3 for i in x]
    y = [i * 1.1 for i in y]


    # Create a Scatter trace for the text labels
    text_trace = go.Scatter(
        x=x,
        y=y,
        mode='text',  # Display text
        text=labels,  # Set text to display
        textposition='middle center',  # Position text in the middle of the polygon
        textfont=dict(size=10, color='black')  # Set text font size and color  
    )
    return text_trace
    




