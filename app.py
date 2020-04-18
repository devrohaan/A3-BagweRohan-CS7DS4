import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

from Constants import TITLE, NAME, TCD_ID, COURSE, DESC, MODULE
from visualization_helper import data_preprocess, get_dropdown_features, get_marker_list, get_country_list, \
    get_player_attributes, get_player_skills, get_goalkeeper_attributes

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.title = '19314431-CS7DS4-RohanBagwe'
server = app.server

colors = {
    'background': '#111111',
    'text': '#404040'
}

# loading data
data = pd.read_csv("data_1000_top_players.csv")

# preprocess data
clean_data = data_preprocess(data)

# fetch Drop down choices
features, opts = get_dropdown_features()

# get list of countries
country_list = get_country_list(clean_data)

# fetch marker list
marker_list = get_marker_list()

# fetch radarplot categories
player_attributes = get_player_attributes()
player_skills, clean_data = get_player_skills(clean_data)
goalkeeper_attributes = get_goalkeeper_attributes()

app.layout = html.Div([

    html.Div([

        html.Div([
            html.H4(className="title", children=TITLE),
            html.P(className="self", children=NAME),
            html.P(className="self", children=TCD_ID),
            html.P(className="self", children=COURSE),
            html.P(className="self", children=MODULE),
            html.P(className="assignment_desc", children=DESC),
        ],
            style={'color': 'black',
                   'border-radius': '1px',
                   'padding': '5px',
                   'backgroundColor': 'white',
                   'margin-bottom': '7px',
                   'margin-right': '10px'})
    ],
        style={'backgroundColor': '#e6e2e2', 'padding': '10px 10px'}
    ),

    html.Div([
        html.P([
            html.Label(id="labelx", children="X-axis:"),
            dcc.Dropdown(id='x-axis-feature',
                         options=opts,
                         value='Age',
                         style={'width': '300px',
                                'fontSize': '15px',
                                'padding-right': '4%',
                                'color': 'black',
                                'display': 'inline-block'
                                }
                         ),

            html.Img(
                id="logo",
                src=app.get_asset_url('logo.png'),
                style={'width': '250px'}),
            
            html.Label(id="labely", children="Y-axis:"),
            dcc.Dropdown(id='y-axis-feature',
                         options=opts,
                         value='Value (million, €)',
                         style={'width': '300px',
                                'fontSize': '15px',
                                'padding-left': '0%',
                                'color': 'black',
                                'display': 'inline-block'}),
        ]),
    ], style={'width': '100%', 'display': 'inline-block', 'text-align': 'center', 'padding': '0 20'}),

    html.Div([
        dbc.Card(
            [
                dbc.CardImg(id="player_info_card", top=True),
                dbc.CardBody(
                    [
                        html.H4(id="player_name"),
                        html.Img(id="player_national_flag", className="flag"),
                        html.H2(id="player_summary", children="data"),
                    ]
                ),
            ],
            style={"padding-top": "50px", "text-align": "center", "width": "100%", 'display': 'inline-block',
                   "background": "white"},
        ),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.Img(id="player_club_logo", className="club_logo",
                                 style={"float": "left", "padding": "17px", "padding-left": "4vw"}),
                        html.Label(id="player_club_name", className="player_club_info",
                                   style={'display': 'inline-block'}),
                        html.Label(id="player_club_joining", className="player_club_info"),
                        html.Label(id="player_club_release_clause", className="player_club_info"),
                        html.Label(id="player_international_reputation", className="player_club_info")
                    ]
                ),
            ],
            style={"padding-top": "40px", "padding-bottom": "66px", "width": "100%", 'display': 'inline-block',
                   "background": "white"},
        ),
        dcc.Graph(id='player-stats', ),

    ], id="dashboard", style={'float': 'left', 'display': 'inline-block', 'width': '40%', 'margin-left': '13px'}),

    html.Div([
        dcc.Graph(
            id='fifa-scatter',
            hoverData={'points': [{'text': 'Cristiano Ronaldo'}]},
        ),
        dcc.Slider(
            id='fifa-scatter-player-count',
            min=min(marker_list),
            max=max(marker_list),
            value=50,
            step=None,
            marks={str(count): str(count) for count in marker_list},
        ),
        dcc.Graph(id='player-geo-locations', )
    ], style={'display': 'inline-block', 'width': '58%'}),

])


@app.callback(
    dash.dependencies.Output('fifa-scatter', 'figure'),
    [dash.dependencies.Input('x-axis-feature', 'value'),
     dash.dependencies.Input('y-axis-feature', 'value'),
     dash.dependencies.Input('fifa-scatter-player-count', 'value'), ])
def update_players_profile_scatter(x_axis_value, y_axis_value, slider_value):
    data = clean_data[:slider_value]
    trace1 = [
        dict(
            x=data[data['Nationality'] == i][x_axis_value],
            y=data[data['Nationality'] == i][y_axis_value],
            text=data[data['Nationality'] == i]['Name'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ) for i in data.Nationality.unique()
    ]
    title = "Choose comparison criteria above!<br><b>Comparing Top " + str(slider_value) + "/1000 players\' " + x_axis_value + " Vs. " + y_axis_value +"</b>".upper()
    layout = dict(
        title={"text": title, "font": {"size": 15}},
        xaxis={'type': 'linear', 'title': "<b>"+x_axis_value+"</b>"},
        yaxis={'title': "<b>"+y_axis_value+"</b>"},
        margin={'l': 40, 'b': 40, 't': 60, 'r': 10},
        legend={'x': 1, 'y': 0},
        font={'color': colors['text'], "family": "Roboto, sans-serif",},
        hovermode='closest',
        height=413,
    )
    fig = go.Figure(data=trace1, layout=layout)
    return fig


@app.callback(
    dash.dependencies.Output('player-geo-locations', 'figure'),
    [dash.dependencies.Input('fifa-scatter', 'hoverData'),
     dash.dependencies.Input('y-axis-feature', 'value'),
     dash.dependencies.Input('fifa-scatter-player-count', 'value')])
def update_player_geo_location(hoverData, y_axis_feature, slider_value):
    player_name = hoverData['points'][0]['text']
    player_data = clean_data.loc[clean_data['Name'] == player_name]
    data = clean_data[:slider_value]
    trace1 = {
        "type": "scattergeo",
        "locations": player_data.Nationality_ISO_alpha,
        "opacity": 0.9,
        "mode": "markers",
        "marker": {
            'size': 10,
            "color": "orange",
            "symbol": "diamond",
            "line": {
                "color": 'black',
                "width": 3}
        },
        "hoverinfo": 'text+name',
        "name": player_data.Nationality.values[0],
        "text": player_data.Name + ",<br>" + y_axis_feature + ": " + str(
            player_data[y_axis_feature].values[0]) + ",<br>Country Average " + y_axis_feature + ": " + str(round(
            data[data['Nationality'] == player_data.Nationality.values[0]][y_axis_feature].mean(), 2)),
        "showlegend": False,
    }
    trace2 = {
        "type": "choropleth",
        "z": data[y_axis_feature].tolist(),
        "text": data.Nationality,
        "hoverinfo": 'text',
        "locations": data.Nationality_ISO_alpha,
        "name": str(y_axis_feature),
        "hoverlabel": {"bgcolor": "white", },
        "colorbar": go.choropleth.ColorBar(title=str(y_axis_feature), xanchor="left"),
        "colorscale": px.colors.sequential.Sunset,
    }
    layout = {

        "geo": {
            "showframe": False,
            "showcoastlines": True,
            "showocean": True,
            "landcolor": "#d8d8d8",
            "oceancolor": "#cef6f7",
            "projection": go.layout.geo.Projection(type='equirectangular'),
        },

        "title": {"text": "<b>Average " + str(y_axis_feature) + " of a footballer in " + player_data.Nationality.values[
            0] + " : " + str(round(
            data[data['Nationality'] == player_data.Nationality.values[0]][y_axis_feature].mean(), 2)) + "</b>",
                  "font": {"size": 15}, },
        "margin": {'l': 40, 'b': 40, 't': 100, 'r': 10, },
        "font": {'color': colors['text'], "family": "Roboto, sans-serif",},
        "autosize": True,
    }
    fig = go.Figure(data=[trace1, trace2], layout=layout)
    return fig


@app.callback(
    dash.dependencies.Output('player_info_card', 'src'),
    [dash.dependencies.Input('fifa-scatter', 'hoverData')])
def render_player_info_card(hoverData):
    player_name = hoverData['points'][0]['text']
    player_data = clean_data.loc[clean_data['Name'] == player_name]
    photo_url = player_data['Photo'].values[0]
    image_name = photo_url.split("/")[-1]
    return app.get_asset_url('top_1000_players/' + image_name)


@app.callback(
    dash.dependencies.Output('player_name', 'children'),
    [dash.dependencies.Input('fifa-scatter', 'hoverData')])
def render_player_name(hoverData):
    player_name = hoverData['points'][0]['text']
    return player_name


@app.callback(
    dash.dependencies.Output('player_national_flag', 'src'),
    [dash.dependencies.Input('fifa-scatter', 'hoverData')])
def render_player_national_flag(hoverData):
    player_name = hoverData['points'][0]['text']
    player_data = clean_data.loc[clean_data['Name'] == player_name]
    photo_url = player_data['Flag'].values[0]
    image_name = photo_url.split("/")[-1]
    return app.get_asset_url('top_1000_flags/' + image_name)


@app.callback(
    dash.dependencies.Output('player_club_logo', 'src'),
    [dash.dependencies.Input('fifa-scatter', 'hoverData')])
def render_player_club_logo(hoverData):
    player_name = hoverData['points'][0]['text']
    player_data = clean_data.loc[clean_data['Name'] == player_name]
    photo_url = player_data['Club Logo'].values[0]
    image_name = photo_url.split("/")[-1]
    return app.get_asset_url('top_1000_clubs/' + image_name)


@app.callback(
    dash.dependencies.Output('player_summary', 'children'),
    [dash.dependencies.Input('fifa-scatter', 'hoverData')])
def render_player_summary(hoverData):
    player_name = hoverData['points'][0]['text']
    player_data = clean_data.loc[clean_data['Name'] == player_name]
    overall = player_data['Overall'].values[0]
    Potential = player_data['Potential'].values[0]
    wage = player_data['Wage'].values[0]
    value = player_data['Value'].values[0]
    description = "Overall Rating: {}  |  Potential:{}  |  Wage: {}  |  Value: {} ".format(str(overall), str(Potential),
                                                                                           str(wage), str(value))
    return description


@app.callback(
    dash.dependencies.Output('player_club_name', 'children'),
    [dash.dependencies.Input('fifa-scatter', 'hoverData')])
def render_player_club_name(hoverData):
    player_name = hoverData['points'][0]['text']
    player_data = clean_data.loc[clean_data['Name'] == player_name]
    club_name = player_data['Club'].values[0]
    if club_name == 0: club_name = "Missing"
    jersey_number = int(player_data['Jersey Number'].values[0])
    if jersey_number == 0: jersey_number = "Missing"
    description = "Club Name: {} | Jersey Number: {}".format(str(club_name), str(jersey_number))
    return description


@app.callback(
    dash.dependencies.Output('player_club_joining', 'children'),
    [dash.dependencies.Input('fifa-scatter', 'hoverData')])
def render_player_joining(hoverData):
    player_name = hoverData['points'][0]['text']
    player_data = clean_data.loc[clean_data['Name'] == player_name]
    joining = player_data['Joined'].values[0]
    if joining == 0: joining = "Missing"
    contact_validity = player_data['Contract Valid Until'].values[0]
    if contact_validity == 0: contact_validity = "Missing"
    description = "Joining: {} | Contact Validity: {}".format(str(joining), str(contact_validity))
    return description


@app.callback(
    dash.dependencies.Output('player_club_release_clause', 'children'),
    [dash.dependencies.Input('fifa-scatter', 'hoverData')])
def render_player_release_clause(hoverData):
    player_name = hoverData['points'][0]['text']
    player_data = clean_data.loc[clean_data['Name'] == player_name]
    position = player_data['Position'].values[0]
    if position == 0: position = "Missing"
    release_clause = player_data['Release Clause'].values[0]
    if release_clause == 0: release_clause = "Missing"
    description = "Playing Position: {} | Release Clause: {}".format(str(position), str(release_clause))
    return description


@app.callback(
    dash.dependencies.Output('player_international_reputation', 'children'),
    [dash.dependencies.Input('fifa-scatter', 'hoverData')])
def render_player_release_clause(hoverData):
    player_name = hoverData['points'][0]['text']
    player_data = clean_data.loc[clean_data['Name'] == player_name]
    pref_foot = player_data['Preferred Foot'].values[0]
    if pref_foot == 0: pref_foot = "Missing"
    international_reput = player_data['International Reputation'].values[0]
    if international_reput == 0: international_reput = "Missing"
    description = "Preferred Foot: {} | International Reputation: {}".format(str(pref_foot), str(international_reput))
    return description


@app.callback(
    dash.dependencies.Output('player-stats', 'figure'),
    [dash.dependencies.Input('fifa-scatter', 'hoverData')])
def render_player_attributes(hoverData):
    player_name = hoverData['points'][0]['text']
    player_data = clean_data.loc[clean_data['Name'] == player_name]
    player_attributes_data_row = player_data[player_attributes]
    player_skills_data_row = player_data[player_skills]
    goalkeeper_attributes_data_row = player_data[goalkeeper_attributes]

    trace_1 = go.Scatterpolar(r=player_attributes_data_row.values.tolist()[0],
                              theta=player_attributes,
                              name='Attributes',
                              fill='toself',
                              line=dict(color='orange')
                              )

    trace_2 = go.Scatterpolar(r=player_skills_data_row.values.tolist()[0],
                              theta=player_skills,
                              name='Skills',
                              visible='legendonly',
                              fill='toself',
                              line=dict(color='blue')
                              )

    trace_3 = go.Scatterpolar(r=goalkeeper_attributes_data_row.values.tolist()[0],
                              theta=goalkeeper_attributes,
                              name='Goalkeeping',
                              fill='toself',
                              visible='legendonly',
                              line=dict(color='green')
                              )
    layout = go.Layout(title=dict(text="<b>"+player_name + '\'s Stats'+"</b>", font=dict(size=15)),
                       font_size=9.5,
                       height=450,
                       margin={'l': 10, 'b': 30, 't': 100, 'r': 0},
                       hovermode='closest',
                       polar=dict(
                           radialaxis=dict(
                               visible=True,
                               range=[0, 100]
                           )
                       ),
                       font={'color': colors['text'], "family": "Roboto, sans-serif",},
                       showlegend=True,
                       )
    fig = go.Figure(data=[trace_1, trace_2, trace_3], layout=layout)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)
