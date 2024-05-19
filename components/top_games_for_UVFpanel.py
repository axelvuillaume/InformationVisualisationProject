from dash import dcc
import plotly.graph_objs as go

def generate_topgames(games_data_frame, color, nbgames=5):
    top_games = games_data_frame.head(nbgames)

    hover_text = [f"{game}<br>Playtime: {playtime // 60} hours {playtime % 60} minutes" 
                  for game, playtime in zip(top_games['name'], top_games['playtime_forever'])]

    # Create a horizontal bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(y=top_games['name'],                                            # Game names on y-axis
                         x=top_games['playtime_forever']/60,                             # Playtime on x-axis
                         orientation='h',                                                # Horizontal orientation
                         marker=dict(color=color),                                       # Bar color
                         text=top_games['name'],                                         # Display game names on the bars
                         textposition='inside',                                          # Position text inside the bars
                         hoverinfo='text',                                               # Display custom hover text
                         hovertext=hover_text,                                           # Set custom hover text
                        ))
    
    # Customize layout
    fig.update_layout(xaxis_title="Playtime (hours)",                                    # X-axis title
                      yaxis_title="",                                                    # No Y-axis title
                      yaxis=dict(autorange="reversed", showticklabels=False),            # Reverse the y-axis and hide tick labels
                      margin=dict(l=1, r=1, t=10, b=1),                                  # Adjust margins for better visibility
                      width=450,
                      height=440
                     )

    return dcc.Graph(figure=fig)