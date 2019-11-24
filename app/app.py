# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 10:30:00 2019

@author: svasquez
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

# this code leverages this resource - https://dash.plot.ly/getting-started

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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
The highest proportion of trees are in good health.
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
    html.H1(children='Silverio J. Vasquez - Module #4'),  
        html.Div(children=[
    html.H2(children='Answer to Question #1'),
    dcc.Markdown(children=answer_1),  
    generate_table(soql_trees_health)
        ]),
    
        html.Div(children=[
    html.H2(children='Answer to Question #2'),
     dcc.Markdown(children=answer_2),        
    html.H4(children='Number of trees regarded as Fair grouped by Steward'),
    generate_table(soql_trees_steward_fair)
        ]),
    
        html.Div(children=[
    html.H4(children='Number of trees regarded as Good grouped by Steward'),
    generate_table(soql_trees_steward_good)
        ]),
        
        html.Div(children=[
    html.H4(children='Number of trees regarded as Poor grouped by Steward'),
    generate_table(soql_trees_steward_poor)
        ])
])

if __name__ == '__main__':
    app.run_server(debug=True)