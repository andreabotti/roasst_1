import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

# from roasst.app import app
from roasst import urls
from roasst.models import df_acr_large

##########
# DASH APP

# Setup app
app = dash.Dash(name='app2', sharing=True,
                server=None)
app.config.supress_callback_exceptions = True

# CSS
external_css = ["https://fonts.googleapis.com/css?family=Overpass:300,300i",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/dab6f937fd5548cebf4c6dc7e93a10ac438f5efb/dash-technical-charting.css",
                "https://codepen.io/chriddyp/pen/bWLwgP.css"]
[app.css.append_css({"external_url": css}) for css in external_css]
if 'DYNO' in os.environ:
    app.scripts.append_script({
                                  'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'})

app.layout = html.Div([
    html.H1('ROASST App - Explore simulation results'),
    html.Div(
        [
            html.Div([
                html.H4('DataTable'),
                dt.DataTable(
                    id='acr_table',
                    rows=df_acr_large.to_dict('records'),
                    # columns=col_sel,     # optional - sets the order of columns
                    filterable=True,
                    sortable=True,
                    row_selectable=True,
                    selected_row_indices=[],
                ),
            ], className='six columns',
            ),
            html.Div(id='selected-indexes', children=[
                html.H4('Chart'),
                dcc.Graph(
                    id='acr_graph'
                )
            ], className='five columns',
                     ),
        ], className='row',
        style={
            'fontSize': 11,
            'background-color': '#F3F3F3',
            'font-family': 'overpass',
            'width': '90%', 'max-width': '1500',
            'margin-left': 'auto', 'margin-right': 'auto', 'padding': '20', 'padding-top': '20', 'padding-bottom': '20',
        },
    )
])


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


if __name__ == '__main__':
    app.run_server(port=8053, debug=False)
