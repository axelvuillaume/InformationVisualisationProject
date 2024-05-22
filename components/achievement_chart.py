from dash import dcc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from utils.load_data import current_user
from utils.data_processing import get_achievements_for_game
from datetime import datetime

def achievement_chart(app_id, game_name):

    if(app_id is not None):
        achievement_data = get_achievements_for_game(current_user.steamid , app_id)
        global_achievements = achievement_data['global_achievements']
        achievement_list = [{"global_percent": [g_achievement['percent'] for g_achievement in global_achievements if g_achievement['name'] == achievement['apiname']][0], 
                            "name": achievement['name'], "unlocktime": achievement['unlocktime'], 
                            "unlocktime_datetime": datetime.fromtimestamp(achievement['unlocktime']).strftime('%d/%m/%y %H:%M'), 
                            "unlocktime_day": datetime.fromtimestamp(achievement['unlocktime']).strftime('%d/%m/%y') } 
                            for achievement in achievement_data['achievements'] 
                            if achievement['achieved'] == 1]
        if achievement_list:
            achievement_df = pd.DataFrame(achievement_list)
            achievement_df.sort_values('unlocktime', ascending=True, inplace=True)
            achievement_df['achievement_index'] = range(1, len(achievement_df) + 1)
            # achievement_df['percentage_rank_symbols'] = achievement_df['global_percent'].map(
            #     lambda x: 1 if(x <= 1)
            #     else 2 if (x <= 5) 
            #     else 3 if (x <= 10) 
            #     else 4 if (x <= 50) 
            #     else 5)
            # achievement_df['percentage_rank_colors'] = achievement_df['global_percent'].map(
            #     lambda x: "#003f5c" if(x <= 1)
            #     else "#58508d" if (x <= 5) 
            #     else "#bc5090" if (x <= 10) 
            #     else "#ff6361" if (x <= 50) 
            #     else "#ffa600")
            # # used this to decide the colors https://www.learnui.design/tools/data-color-picker.html#palette
            achievement_df['percentage_rank_name'] = achievement_df['global_percent'].map(
                lambda x: "very rare (0%, 1%]" if(x <= 1)
                else "rare (1%, 5%]" if (x <= 5) 
                else "uncommon (5%, 10%]" if (x <= 10) 
                else "common (10%, 50%]" if (x <= 50) 
                else "very common (50%, 100%]")

            # Alternate version with lines
            # fig = px.line(achievement_df, x='unlocktime_datetime', y='global_percent', 
            #             #   color="percentage_rank_name",  
            #               markers=True, 
            #               #text=achievement_df['name']
            #               )
            # fig.update_traces(marker=dict(size=12, 
            #                                color=achievement_df['percentage_rank_colors'], 
            #                                symbol=achievement_df['percentage_rank_symbols'],
            #                             #   cmin=1, 
            #                             #   cmax=5
            #                               ),
            #                     textposition="bottom right")

            fig = px.scatter(achievement_df, x='unlocktime_day', y='global_percent', 
                            color="percentage_rank_name",
                            symbol="percentage_rank_name",
                            category_orders={"percentage_rank_name": 
                                            ["very rare (0%, 1%)",
                                            "rare (1%, 5%)",
                                            "uncommon (5%, 10%)",
                                            "common (10%, 50%)",
                                            "very common (50%, 100%)"]},
                            color_discrete_sequence=px.colors.qualitative.Bold,
                            hover_data={"name": True, "unlocktime_datetime": True, "unlocktime_day": False},
                            labels={"percentage_rank_name": "Rarity", "unlocktime_day": "Unlocked date",  "unlocktime_datetime": "Unlock time", 'global_percent': "Global Percentage", "name": "Achievement Name"}
                            # text=achievement_df['name']
                            )
            fig.update_traces(marker=dict(size=12,
                                        #   color=achievement_df['percentage_rank_colors'], 
                                        ),
                                # textposition="bottom right",
                                showlegend=True)
            
            fig.update_xaxes(tickangle=45)

            fig.update_layout(yaxis=dict(autorange="reversed"), yaxis_title="Global Percentage", xaxis_title="Unlock Time (date)", title=f"Achievement timeline for {game_name}")
            return dcc.Graph(id='achievement-chart-figure', figure=fig)
        
    # if nothing was returned before this, return an empty graph
    fig = go.Figure()
    fig.update_layout(title="No achievements found")
    return dcc.Graph(id='achievement-chart-figure', figure=fig)
