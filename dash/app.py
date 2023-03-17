from dash import Dash, dcc, html, Input, Output, State
import dash
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import pandas as pd
import sys
import os
sys.path.append(os.path.join(sys.path[0], '..','src'))
from graph_api import build_graph

#app = Dash(__name__)

df_txb = pd.read_json('../dat/textbooks/graph.json')
df_wiki = pd.read_json('../dat/wiki/graph.json')
df_llm = pd.read_json('../dat/llm/graph.json')

#internal_concepts = df_concepts.concept.to_list()

concept = "Eigenvalues and eigenvectors"
elements=build_graph(df_llm,dep_column = "dep_articles",concept=concept,depth=2)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


controls = dbc.Card(
    [   
        html.Div( 
            [
                html.Datalist(
                    id='list-suggested-inputs', 
                    children=[html.Option(value=word) for word in df_wiki.concept]
                    ),
                html.H6("Choose a source of data"),
                dcc.RadioItems(['Textbooks','Wikipedia','Large Language Model'],
                    value = 'Large Language Model',
                    id='radioitems'
                ),
                html.H6(""),
                html.H6("Type a concept"),
                dcc.Input(id="input_concept",
                    placeholder='Enter a concept...',
                    type='text',
                    value=concept,
                    list='list-suggested-inputs'
                ),
                 html.H6(""),
                html.H6("Choose the depth of dependencies"),
                dcc.Dropdown([1,2,3,4,5,6,7,8,9,10],
                            value = 2,
                            id ='input_depth'
                             ),
                html.Button('Submit', id='button')
            ]
        )   
    ],
    body=True,
)


app.layout = dbc.Container(
    [
        html.H1("Concept Dependencies Graph"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=3),
                dbc.Col(   cyto.Cytoscape(
                            id='graph',
                            elements=elements,
                            layout={'name': 'breadthfirst','roots': '[id = "Eigenvalues and eigenvectors"]'},
                            style={'width': '1000px', 'height': '800px'},
                            stylesheet=[
                            {
                                'selector': 'node',
                                'style': {'content': 'data(label)',
                                        'text-halign':'center',
                                        'text-valign':'center',
                                        'text-margin-y' : '-20px'}
                                
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
    


@app.callback(
    Output('graph', 'layout'),
    Output('graph', 'elements'),
    Input('button','n_clicks'),
    State('radioitems','value'),
    State('input_concept','value'),
    State('input_depth','value')
)

def update_elements(n_clicks,source,concept,depth):
    if source == "Textbooks":
        elements=build_graph(df_txb,dep_column = "dep_articles",concept=concept,depth=depth)

    if source == "Large Language Model":
        elements=build_graph(df_llm,dep_column = "dep_articles",concept=concept,depth=depth)

    if source == "Wikipedia":
        elements=build_graph(df_wiki,dep_column = "dep_articles",concept=concept,depth=depth)

    layout = {'name': 'breadthfirst','roots': f'[id = "{concept}"]'}
    return layout, elements



if __name__ == '__main__':
    app.run_server(debug=True)