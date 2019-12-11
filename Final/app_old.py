# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 10:30:00 2019

@author: svasquez
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import pandas as pd
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
from fredapi import Fred

# this code leverages this resource - https://dash.plot.ly/getting-started

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
fred = Fred(api_key='0d3a129121b29e16035b20ea3947ecf5')


soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=health,count(tree_id)' +\
        '&$group=health').replace(' ', '%20')
soql_trees_health = pd.read_json(soql_url)
soql_trees_health['pct_contr'] = soql_trees_health['count_tree_id']/soql_trees_health['count_tree_id'].sum()*100

health = 'Fair'
soql_fair = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=steward,count(tree_id)' +\
        "&$where=health='"+health +"'"\
        '&$group=steward').replace(' ', '%20')
soql_trees_steward_fair = pd.read_json(soql_fair)

health = 'Good'
soql_good = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=steward,count(tree_id)' +\
        "&$where=health='"+health +"'"\
        '&$group=steward').replace(' ', '%20')
soql_trees_steward_good = pd.read_json(soql_good)

health = 'Poor'
soql_poor = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=steward,count(tree_id)' +\
        "&$where=health='"+health +"'"\
        '&$group=steward').replace(' ', '%20')
soql_trees_steward_poor = pd.read_json(soql_poor)

answer_1 = '''
My final project plots data sourced from the St. Louis Federal Reserve.
A user can select the desired economic variable. This Dash app will then
plot the selected variable in an interactive chart and a small multiple will
show the selected variable plotted against other important macroeconomic 
variables, such as real GDP, nominal GDP, and core inflation YoY%.
'''

answer_2 = '''
It's too difficult to ascertain if steward has an affect on health
because there are many trees without steward information.
'''

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app.layout = html.Div([
    html.H1(children='Silverio J. Vasquez - Data 608 - Final Project'),  
        html.Div(children=[
    html.H2(children='Overview2'),
    dcc.Markdown(children=answer_1),  
    generate_table(soql_trees_health)
        ]),  
        
    html.H2(children='Multi-Select Dropdown'),    
    html.Div(id='dd-output-container'), 
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Growth', 'value': 'GDP'},
            {'label': 'Inflation', 'value': 'CPI'},
            {'label': 'Wages', 'value': 'AHE'}
        ],
        placeholder="Select an economic indicator",
        multi=True,
        clearable=False
    ),
        html.Div([
        #dcc.Graph(id='graph'),
        dt.DataTable(id='data-table', columns=[
            {'name': 'Title', 'id': 'title'},
            {'name': 'Score', 'id': 'score'}
        ])
    ])
])
    
@app.callback(
    [Output('dd-output-container', 'children'),
     Output('data-table','data'),
     Output('data-table','columns')],
    [Input('demo-dropdown', 'value')])

def update_output(value):

    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)
