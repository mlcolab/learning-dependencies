from dash import Dash, dcc, html, Input, Output, State
import dash
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import pandas as pd
import sys
import os
sys.path.append(os.path.join(sys.path[0],'..', '..','src'))
import graph_api 

#app = Dash(__name__)

df_concepts = pd.read_json('dat/wiki/graph.json')   
internal_concepts = df_concepts.concept.to_list()

value = "Eigenvalues and eigenvectors"
deps = df_concepts.loc[df_concepts.concept==value,"deps"].to_list()[0]
df = df_concepts.loc[df_concepts.concept.isin([value]+deps)]
elements=graph_api.build_graph(df.concept, df.deps, internal_concepts)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


controls = dbc.Card(
    [   html.Div( 

            [html.H5("Type a concept"),
            html.Datalist(
                         id='list-suggested-inputs', 
                          children=[html.Option(value=word) for word in internal_concepts]),
                dcc.Input(id="input_concept",
                    placeholder='Enter a concept...',
                    type='text',
                    value=value,
                    list='list-suggested-inputs'),
            html.Button('Submit', id='button', n_clicks=0)
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
                            layout={'name': 'cose'},
                            style={'width': '1000px', 'height': '700px'},
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
                            },
                                        {
                                'selector': '.blue',
                                'style': {
                                'background-color': 'blue',
                                'line-color': 'blue'
                }
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
              Input('button','n_clicks'),
              State('input_concept','value'))

def update_elements(n_clicks,value):

    deps = df_concepts.loc[df_concepts.concept==value,"deps"].to_list()[0]
    df = df_concepts.loc[df_concepts.concept.isin([value]+deps)]
    elements=graph_api.build_graph(df.concept, df.deps, internal_concepts)

    return elements



if __name__ == '__main__':
    app.run_server(debug=False)