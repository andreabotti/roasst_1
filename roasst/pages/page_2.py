import plotly.graph_objs as go

import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

from roasst.app import app
from roasst.models import df_acr_large, df_acr_large


col_sel = ['job_id', '@model', '@weather', '@north', '@floor', '@ach', '@wwr_KL', '@wwr_B', 'BD1_HA26p_occ']


datatable = html.Div([
    html.H4('Sergey'),
    dt.DataTable(
        id='acr_table',
        rows=df_acr_large.to_dict('records'),
        columns=col_sel,  # optional - sets the order of columns
        filterable=True,
        sortable=True,
        row_selectable=True,
        selected_row_indices=[],
    ),
], className='six columns', )

graph = html.Div(id='selected-indexes', children=[

    html.H4('Chart'),
    dcc.Graph(id='acr_graph')
],
                 className='five columns',
                 )

page_2_layout = html.Div(
    [
        html.H1('ROASST App - Explore simulation results'),
        datatable,
        graph,

    ],
    className='row',
    style={
        'fontSize': 11,
        'background-color': '#F3F3F3',
        'font-family': 'overpass',
        'width': '90%', 'max-width': '1500',
        'margin-left': 'auto', 'margin-right': 'auto', 'padding': '20', 'padding-top': '20', 'padding-bottom': '20',
    },
)


@app.callback(
    Output('acr_table', 'selected_row_indices'),
    [Input('acr_graph', 'clickData')],
    [State('acr_table', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


@app.callback(
    Output('acr_graph', 'figure'),
    [Input('acr_table', 'rows'), Input('acr_table', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    data = go.Data([])
    marker = {'color': ['#0074D9'] * len(dff)}
    for i in (selected_row_indices or []):
        marker['color'][i] = '#FF851B'
    data.append(
        go.Bar(
            x=df_acr_large['BD1_HA26p_occ'],
            y=df_acr_large['job_id'],
            orientation='h',
            marker=marker,
        ),
    ),

    figure = go.Figure(
        data=data,
        # layout=layout,
    )
    return figure
