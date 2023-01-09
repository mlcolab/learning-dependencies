from dash import Dash, dcc, html, Input, Output
import dash
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import json

#app = Dash(__name__)
with open('data/wiki_graph_all.json') as f:
    elements = json.load(f) 

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

controls = dbc.Card(
    [   html.Div( 

            [
                dcc.Dropdown( id = 'dropdown',
                    options = [
                        {'label':'all', 'value':'all' },
                        {'label': 'known', 'value':'known'}
                        ],
                    value = 'all')
            ]
                    )
    
            ],
    body=True,
)


app.layout = dbc.Container(
    [
        html.H1("Wikipedia graph"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=2),
                dbc.Col(   cyto.Cytoscape(
                            id='graph',
                            elements=elements,
                            layout={'name': 'random'},
                            style={'width': '900px', 'height': '700px'}
    )
),
            ],
            align="center",
        ),
    ],
    fluid=True,
)
    


@app.callback(Output('graph', 'elements'),
              Input('dropdown', 'value'))

def update_elements(value):
    if value == "all":
        with open('data/wiki_graph_all.json') as f:
            elements = json.load(f) 
    else:
        with open('data/wiki_graph_known.json') as f:
            elements = json.load(f) 

    return elements



if __name__ == '__main__':
    app.run_server(debug=True)