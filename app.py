import base64
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import pycountry
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.title = 'Rohan Bagwe'
server = app.server

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# loading data
data = pd.read_csv("data.csv")
data["Flag"] = data["Flag"].str.replace(".org/", ".com/", case=False)
data["Photo"] = data["Photo"].str.replace(".org/", ".com/", case=False)
features = data.columns[1:-1]
opts = [{'label': i, 'value': i} for i in features]

app.layout = html.Div([

    html.Div([

        html.Div([
            html.H1("1WERTYUI"),
            html.P("1")
        ],
            style={'color': 'black',
                   'border-radius': '10px',
                   'padding': '5px',
                   'backgroundColor': 'white',
                   'margin-bottom': '5px'})
    ],
        style={'backgroundColor': '#d2d0d0', 'padding': '10px 10px'}
    ),

    html.Div([
        html.P([
            dcc.Dropdown(id='choosefeatre',
                         options=opts,
                         value='ID',
                         style={'width': '100px',
                                'fontSize': '20px',
                                'padding-top': '10px',
                                'display': 'inline-block'}),

            dcc.Dropdown(id='choosefeatrex',
                         options=opts,
                         value='ID',
                         style={'width': '100px',
                                'fontSize': '20px',
                                'padding-top': '10px',
                                'display': 'inline-block'}),

            html.Img(
                id="player_profile_picture",
                style={'width': '70px'}),

            dcc.Dropdown(id='choosefeatrexd',
                         options=opts,
                         value='ID',
                         style={'width': '100px',
                                'fontSize': '20px',
                                'padding-top': '10px',
                                'display': 'inline-block'}),

            dcc.Dropdown(id='choosesfeatrexd',
                         options=opts,
                         value='ID',
                         style={'width': '100px',
                                'fontSize': '20px',
                                'padding-top': '10px',
                                'display': 'inline-block'}),
        ]),
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),

    html.Div([
        dbc.Card(
            [
                dbc.CardImg(id="card", src=data["Photo"][0], top=True, style={"width": "70px"}),
                dbc.CardBody(
                    [
                        html.H4("Card title", className="card-title"),
                        html.P(
                            "Some quick example text to build on the card title and "
                            "make up the bulk of the card's content.",
                            className="card-text",
                        ),
                    ]
                ),
            ],
            style={"width": "100%", 'display': 'inline-block', "background": "white"},
        ),
        dcc.Graph(
            id='fifa-scatter',
            hoverData={'points': [{'default': 'L. Messi'}]},
        ),

    ], id="dashboard", style={'float': 'left','display': 'inline-block', 'width': '49%', 'margin-left': '13px'}),

    html.Div([
        dcc.Graph(id='player_stats',),
        dcc.Graph(id='player_geo_locations',)
    ], style={'display': 'inline-block', 'width': '49%'}),

])

data1 = data[:10]


@app.callback(
    dash.dependencies.Output('fifa-scatter', 'figure'),
    [dash.dependencies.Input('fifa-scatter', 'hoverData')])
def update_player_profile_scatter(hoverData):
    print(hoverData)
    trace_1 = go.Scatter(x=data1.Age,
                         y=data1.Wage,
                         name='AAPL HIGH',
                         mode='markers',
                         text=data1.Name,
                         marker={
                             'size': 20,
                             'opacity': 0.5,
                             'color': 'red',
                             'line': {'width': 0.5, 'color': 'white'}
                         }, )
    layout = go.Layout(title='Players Profile',
                       xaxis={
                           'title': "Column name",
                       },
                       yaxis={
                           'title': "Column name",
                       },
                       margin={'l': 40, 'b': 30, 't': 90, 'r': 90},
                       hovermode='closest',
                       #plot_bgcolor=colors['background'],
                       #paper_bgcolor=colors['background'],
                       #font={'color': colors['text']}
                       )
    fig = go.Figure(data=[trace_1], layout=layout)
    return fig


data.Nationality.replace("England", "United Kingdom", inplace=True)
data.Nationality.replace("Wales", "United Kingdom", inplace=True)
data.Nationality.replace("Scotland", "United Kingdom", inplace=True)
data.Nationality.replace("Northern Ireland", "Ireland", inplace=True)
data.Nationality.replace("Republic of Ireland", "Ireland", inplace=True)
data.Nationality.replace("Korea Republic", "Korea, Democratic People's Republic of", inplace=True)
data.Nationality.replace("China PR", "China", inplace=True)
data.Nationality.replace("Russia", "Russian Federation", inplace=True)
data.Nationality.replace("Ivory Coast", "Côte d'Ivoire", inplace=True)
data.Nationality.replace("Czech Republic", "Czechia", inplace=True)
data.Nationality.replace("DR Congo", "Congo, The Democratic Republic of the", inplace=True)
data.Nationality.replace("Bosnia Herzegovina", "Bosnia and Herzegovina", inplace=True)

data2 = data.copy()

data2["Nationality_temp"] = data.Nationality
for i, row in data2.iterrows():
    if pycountry.countries.get(name=row.Nationality_temp) is not None:
        data2.at[i, 'Nationality_temp'] = pycountry.countries.get(name=row.Nationality_temp).alpha_3
        continue
    if pycountry.countries.get(common_name=row.Nationality_temp) is not None:
        data2.at[i, 'Nationality_temp'] = pycountry.countries.get(common_name=row.Nationality_temp).alpha_3
        continue
    if pycountry.countries.get(official_name=row.Nationality_temp) is not None:
        data2.at[i, 'Nationality_temp'] = pycountry.countries.get(official_name=row.Nationality_temp).alpha_3
        continue

data3 = data2[:10]
@app.callback(
    dash.dependencies.Output('player_geo_locations', 'figure'),
    [dash.dependencies.Input('fifa-scatter', 'hoverData')])
def update_player_geo_location(hoverData):
    print(hoverData)
    trace1 = {
        "type": "scattergeo",
        "text": data3.Nationality,
        "locations": data3["Nationality_temp"],
        "opacity": 0.8,
        "marker": {
                 'size': 15, 'line': {'width': 0.5, 'color': 'white'}
                },
    }
    layout = {
        "geo": {
            "showframe": False,
            "showcoastlines": False
        },
        "title": {"text": "Country with best players FIFA 19"},
        "autosize": True
    }
    fig = go.Figure(data=[trace1], layout=layout)
    return fig


@app.callback(
    dash.dependencies.Output('player_profile_picture', 'src'),
    [dash.dependencies.Input('fifa-scatter', 'hoverData')])
def updateImage(hoverData):
    a = hoverData['points'][0]
    return data.Photo[0]


@app.callback(
    dash.dependencies.Output('player_stats', 'figure'),
    [dash.dependencies.Input('fifa-scatter', 'hoverData')])
def create_time_series(hoverData):
    print(hoverData)
    trace_1 = go.Scatterpolar(r=[14, 24,32,12,19],
                          theta=['Month', 'year', 'we', 'wee', 'fer'],
                          name='Deaths Due to Zymotic disease',
                          fill='toself',
                          line=dict(color='orange')
                        )

    layout = go.Layout(title='Player Attributes',
                       font_size=12,
                       height=450,
                       margin={'l': 0, 'b': 20, 't': 70, 'r': 0},
                       hovermode='closest',
                       polar=dict(
                           radialaxis=dict(
                               visible=True,
                               range=[0, 200]
                           )
                       ),
                       showlegend=True,
                    )
    fig = go.Figure(data=[trace_1], layout=layout)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
