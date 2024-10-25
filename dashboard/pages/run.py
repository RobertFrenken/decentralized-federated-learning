import json
import os.path as osp

import dash
from dash import html, callback, Input, Output
import dash_cytoscape as cyto
from dashboard.components import (SidebarAIO, HeaderAIO, TopologyAIO, DistributionAIO, ActivityAIO, SelectionAIO,
                                  LocalLossAIO, GlobalLossAIO, LocalAccuracyAIO, GlobalAccuracyAIO, IndicatorAIO)
from dashboard.utils import process_data

dash.register_page(__name__, path_template='/run/<run_name>', title=lambda run_name: f'Runs | {run_name}')

graph = cyto.Cytoscape(
        id='cytoscape-elements-basic',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '400px'},
        elements=[
            # The nodes elements
            {'data': {'id': 'one', 'label': 'Node 1'},
             'position': {'x': 50, 'y': 50}},
            {'data': {'id': 'two', 'label': 'Node 2'},
             'position': {'x': 200, 'y': 200}},

            # The edge elements
            {'data': {'source': 'one', 'target': 'two', 'label': 'Node 1 to 2'}}
        ]
    )

def layout(run_name: str = None):

    return html.Div([
        HeaderAIO(),
        SidebarAIO(),
        html.Div([
            graph,
            html.Span([
                DistributionAIO(),
                ActivityAIO(),
                SelectionAIO(),
            ], className='flex space-x-7'),
            html.Span([
                LocalLossAIO(),
                GlobalLossAIO()
            ], className='flex space-x-7'),
            html.Span([
                LocalAccuracyAIO(),
                GlobalAccuracyAIO()
            ], className='flex space-x-7'),
            html.Span([
                IndicatorAIO(),
            ], className='flex space-x-7')
        ], className='flex flex-col space-y-7 w-full min-h-screen p-7 pl-[268px]')
    ], className='relative w-full h-full overflow-hidden')


@callback(
    Output('local-storage', 'data'),
    Input('location', 'pathname'),
    prevent_initial_call=True
)
def update_data(pathname: str):
    if pathname == '/':
        return {}
    file = '{}.json'.format(osp.basename(pathname))
    with open(osp.join('logs/', file)) as json_file:
        data = json.load(json_file)
    data = process_data(data)
    return data
