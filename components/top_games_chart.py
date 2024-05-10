from dash import dcc
from dash import html
import plotly.graph_objs as go

def generate_top_games_chart(data, n=10):
    # Assuming 'data' is a DataFrame containing the Steam games dataset
    top_n_games = data.sort_values(by='average_playtime_forever', ascending=False).head(n)
    
    # Create a bar chart
    trace = go.Bar(
        x=top_n_games['name'],
        y=top_n_games['average_playtime_forever'],
        marker=dict(color='rgb(0, 128, 128)')
    )

    layout = go.Layout(
        title='Top {} Games Based on Average playtime'.format(n),
        xaxis=dict(title='Game'),
        yaxis=dict(title='Average playtime'),
        margin=dict(l=40, r=40, t=40, b=40)
    )

    fig = go.Figure(data=[trace], layout=layout)

    fig.update_layout(modebar_add=["?"])

    return dcc.Graph(
        id='top-games-chart',
        figure=fig
    )
