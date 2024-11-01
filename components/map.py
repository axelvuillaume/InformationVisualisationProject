from dash import Dash, dcc, html, Input, Output, callback

import pandas as pd
import plotly.express as px
from utils.load_data import cleaned_games, genres, current_user,supported_languages
import plotly.graph_objects as go

# Correspondance between languages and pays
lang_to_country = {'English': 'United States',
                   'Dutch': 'Netherlands',
                   'Portuguese - Portugal': 'Portugal',
                   'Indonesian': 'Indonesia',
                   'Hebrew': 'Israel',
                   'Lithuanian': 'Lithuania',
                   'Belarusian': 'Belarus',
                   'Irish': 'Ireland',
                   'Icelandic': 'Iceland',
                   'Catalan': 'Spain',
                   'Latvian': 'Latvia',
                   'Serbian': 'Serbia',
                   'Croatian': 'Croatia',
                   'Estonian': 'Estonia',
                   'Slovak': 'Slovakia',
                   'Basque': 'Spain',
                   'Hindi': 'India',
                   'Bangla': 'Bangladesh',
                   'Malay': 'Malaysia',
                   'Marathi': 'India',
                   'Scots': 'United Kingdom',
                   'Filipino': 'Philippines',
                   'Persian': 'Iran',
                   'Uzbek': 'Uzbekistan',
                   'Urdu': 'Pakistan',
                   'French' : 'France',
                   'Armenian': 'Armenia',
                   'Igbo': 'Nigeria',
                   'Sindhi': 'Pakistan',
                   'Sinhala': 'Sri Lanka',
                   'Cherokee': 'United States',
                   'Galician': 'Spain',
                   'Afrikaans': 'South Africa',
                   'Kannada': 'India',
                   'Luxembourgish': 'Luxembourg',
                   'Gujarati': 'India',
                   'Kyrgyz': 'Kyrgyzstan',
                   'Kazakh': 'Kazakhstan',
                   'Turkmen': 'Turkmenistan',
                   "K'iche'": 'Guatemala',
                   'Kinyarwanda': 'Rwanda',
                   'Tajik': 'Tajikistan',
                   'Odia': 'India',
                   'Welsh': 'United Kingdom',
                   'Konkani': 'India',
                   'Nepali': 'Nepal',
                   'Tigrinya': 'Ethiopia',
                   'Slovenian': 'Slovenia',
                   'Swahili': 'Kenya',
                   'Punjabi (Gurmukhi)': 'India',
                   'Punjabi (Shahmukhi)': 'Pakistan',
                   'Georgian': 'Georgia',
                   'Maori': 'New Zealand',
                   'Wolof': 'Senegal',
                   'Bosnian': 'Bosnia and Herzegovina',
                   'Telugu': 'India',
                   'Tamil': 'India',
                   'Valencian': 'Spain',
                   'Quechua': 'Peru',
                   'Zulu': 'South Africa',
                   'Xhosa': 'South Africa',
                   'Sotho': 'Lesotho',
                   'Sorani': 'Iraq',
                   'Yoruba': 'Nigeria',
                   'Uyghur': 'China',
                   'Tswana': 'Botswana',
                   'Mongolian': 'Mongolia',
                   'Hausa': 'Nigeria',
                   'Dari': 'Afghanistan',
                   'Azerbaijani': 'Azerbaijan',
                   'Amharic': 'Ethiopia',
                   'Albanian': 'Albania',
                   'Assamese': 'India',
                   'Tatar': 'Russia',
                   'Macedonian': 'North Macedonia',
                   'Malayalam': 'India',
                   'Maltese': 'Malta',
                   'Khmer': 'Cambodia',
                   'Italian': 'Italy',
                   'German': 'Germany',
                   'Spanish - Spain': 'Spain',
                   'Japanese': 'Japan',
                   'Portuguese - Brazil': 'Brazil',
                   'Russian': 'Russia',
                   'Simplified Chinese': 'China',
                   'Traditional Chinese': 'China',
                   'Korean': 'South Korea',
                   'Portuguese': 'Portugal',
                   'Danish': 'Denmark',
                   'Polish': 'Poland',
                   'Turkish': 'Turkey',
                   'Czech': 'Czech Republic',
                   'Hungarian': 'Hungary',
                   'Dutch': 'Netherlands',
                   'Ukrainian': 'Ukraine',
                   'Spanish - Latin America': 'Latin America',  # Assuming various Spanish-speaking countries
                   'Arabic': 'Various',  # Arabic-speaking countries are spread across multiple regions
                   'Norwegian': 'Norway',
                   'Romanian': 'Romania',
                   'Swedish': 'Sweden',
                   'Thai': 'Thailand',
                   'Vietnamese': 'Vietnam',
                   'Finnish': 'Finland',
                   'Bulgarian': 'Bulgaria',
                   'Greek': 'Greece',
                   'Korean': 'South Korea',
                   'Hungarian': 'Hungary',
                   'Polish': 'Poland'
                  }


supported_languages['Pays'] = supported_languages['supported_languages'].map(lang_to_country)

counts = supported_languages['Pays'].value_counts().reset_index()
counts.columns = ['Pays', 'number']

games_with_countries = pd.merge(supported_languages, cleaned_games, on='app_id')

top_games = games_with_countries.loc[games_with_countries.groupby('Pays')['average_playtime_forever'].idxmax()]
top_games = top_games[['Pays', 'name', 'average_playtime_forever']]


counts = counts.merge(top_games, on='Pays', how='left')

fig = go.Figure(data=go.Choropleth(locations=counts['Pays'],
                                   z=counts['number'],
                                   locationmode='country names',
                                   colorscale = 'emrld',
                                   colorbar_title='Number of games',
                                    text=counts.apply(lambda row: f"Country: {row['Pays']}<br>Number of games: {row['number']}<br>Top game: {row['name']}<br>Playtime: {row['average_playtime_forever']}", axis=1),
                                    hoverinfo='text'
                                  ))

fig.update_layout(title_text='Number of games by supported languages',
                  geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'),
                 )




def graph_map(): 
    return html.Div([
    dcc.Graph(figure=fig)
])