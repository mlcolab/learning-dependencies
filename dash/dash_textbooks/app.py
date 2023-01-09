from dash import Dash, dcc, html, Input, Output
import dash
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import functions

#app = Dash(__name__)

elements = functions.generate_graph_data(5,0.7)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

controls = dbc.Card(
    [   html.Div( 
            [
                dbc.Label("% of books that contain the link"),   
                dcc.Slider(
                1, # minimum
                10, # maximum
                step = 1,
                value = 5,
                marks={str(step): str(step) for step in range(1,11)},
                id = 'nbook-slider'
                )
            ]
        ), 
        html.Div( 
            [
                dbc.Label("Confidence"),   
                dcc.Slider(
                0.1, # minimum
                1, # maximum
                step = 0.1,
                value = 0.7,
                marks={str(step/10): str(step/10) for step in range(1,11)},
                id = 'confidence-slider'
                )
            ]
       )
        
    ],
    body=True,
)


app.layout = dbc.Container(
    [
        html.H1("Textbook graph"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=2),
                dbc.Col(  cyto.Cytoscape(
                            id='graph',
                            elements=elements,
                            layout={'name': 'random'},
                            style={'width': '900px', 'height': '700px'},
                            stylesheet=[
            {
                'selector': 'node',
                'style': {'content': 'data(label)',
                          'text-halign':'center',
                          'text-valign':'center'}
            },
            {
                'selector': 'edge',
                'style': { 'curve-style': 'straight',
                          'target-arrow-color': 'grey',
                          'target-arrow-shape': 'triangle',}
            }
        ],

                            
    )
),
            ],
            align="center",
        ),
    ],
    fluid=True,
)
    

@app.callback(Output('graph', 'elements'),
              Input('confidence-slider', 'value'),
              Input('nbook-slider', 'value'))
              #Input('btn-remove-node', 'n_clicks_timestamp'),
             # State('graph', 'elements'))

def update_elements(confidence_thr, nbook_thr):
    elements = functions.generate_graph_data(nbook_thr,confidence_thr)

    return elements



if __name__ == '__main__':
    app.run_server(debug=True)