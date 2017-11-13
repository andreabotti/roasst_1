import plotly.plotly as py
import plotly.graph_objs as go

import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt

from dash.dependencies import Input, Output

from roasst.app import app
from roasst import urls
from roasst.models import df_acr_large


##########
U_list = [x for x in sorted(df_acr_large['@model'].unique() ) ]
U_options = [{'label': x, 'value': x} for x in sorted(df_acr_large['@model'].unique() ) ]

F_list = [x for x in sorted(df_acr_large['@floor'].unique() ) ]
F_options = [{'label': x.split('_',1)[0], 'value': x} for x in sorted(df_acr_large['@floor'].unique() ) ]

WB_list = [x for x in sorted(df_acr_large['@wwr_B'].unique() ) ]
WB_options = [{'label': x, 'value': x} for x in sorted(df_acr_large['@wwr_B'].unique() ) ]

WKL_list = [x for x in sorted(df_acr_large['@wwr_KL'].unique() ) ]
WKL_options = [{'label': x, 'value': x} for x in sorted(df_acr_large['@wwr_KL'].unique() ) ]

N_list = [x for x in sorted(df_acr_large['@north'].unique() ) ]
A_list = [x for x in sorted(df_acr_large['@ach'].unique() ) ]
A_options = [{'label': x, 'value': x} for x in sorted(df_acr_large['@ach'].unique() ) ]
##########

##########
# page_1_layout = html.Div([
#     html.H3('App 1'),
#     dcc.Dropdown(
#         id='app-1-dropdown',
#         options=[
#             {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
#                 'NYC', 'MTL', 'LA'
#             ]
#         ]
#     ),
#     html.Div(id='app-1-display-value'),
#     dcc.Link('Go to App 2', href=urls.page_2)
# ])
# ROASST App
page_1_layout = html.Div(
    [
        html.H3('Page 1'),
        dcc.Link('Go back to home', href='/'),
        html.Br(),
        html.H1('ROASST App - Explore simulation results'),

        html.H4('Set input parameters', style={'padding-top': '20'}),
        html.Div([
            # Unit radio
            html.Div([
                html.Label('Unit Type'),
                dcc.RadioItems(
                    id='input_T', options=U_options, value=U_list[0], labelStyle={'display': 'inline-block'}),
            ], className='two columns',
            ),
            # N slider
            html.Div([
                html.Label('Angle from north'),
                dcc.Slider(
                    id='input_N',
                    min=min(N_list), max=max(N_list),
                    step=45, value=N_list[1],
                    # marks={i: '{}°'.format(str(i)) for i in range(0,316,45)},
                    marks={int(i): int(i) for i in N_list},
                )
            ], className='two columns',
            ),
            # F radio
            html.Div([
                html.Label('Floor'),
                dcc.RadioItems(
                    id='input_L', options=F_options, value=F_list[0], labelStyle={'display': 'inline-block'}),
            ], className='two columns',
            ),
            # A slider
            html.Div([
                html.Label('Air Changes per Hour'),
                dcc.Slider(
                    id='input_A',
                    min=min(A_list), max=max(A_list),
                    step=1,
                    value=A_list[1],
                    marks={int(i): '{}ach'.format(i) for i in A_list},
                )
            ], className='three columns',
            ),
            # W slider
            html.Div([
                html.Label('Window-to-wall ratios'),
                dcc.Dropdown(
                    id='input_WB',
                    options=WB_options,
                    value='50_50'
                ),
            ], className='two columns',
            ),
            html.Div([html.Br(), ],
                     ),
        ], className='row', style={'background-color': '#F3F3F3'},
        ),

        html.H4('Charts', style={'padding-top': '40'}),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='chart_bar_runperiod',
                    figure={}
                ),
            ], className='six columns',
            ),
            html.Div([
                dcc.Graph(
                    id='chart_scatter_runperiod',
                    figure={}
                ),
            ], className='three columns',
            ),
            html.Div([
                dcc.Graph(
                    id='chart_scatter_wwr',
                    figure={
                        'data': [go.Scatter(
                            x=df_acr_large.index,
                            y=df_acr_large['BD1_TM52_C1'],
                            mode='lines',
                        )],
                    }
                ),
            ], className='three columns',
            ),
        ], className='row', style={'padding': '10 10 10 10'},
        ),

        html.H4('DataTable', style={'padding-top': '40'}),
        html.Div([
            dt.DataTable(
                rows=df_acr_large.to_dict('records'),
                filterable=True,
                sortable=True,
            ),
        ], className='row',
            style={
                'fontSize': 11,
                'width': '100%',
            },
        ),
    html.Div(id='page-1-content'),
    dcc.Link('Go to App 2', href=urls.page_2)
    ],
    style={
        'background-color': '#F3F3F3',
        'font-family': 'overpass',
        'width': '90%', 'max-width': '1500',
        'margin-left': 'auto', 'margin-right': 'auto', 'padding': '20', 'padding-top': '20', 'padding-bottom': '20',
    },
)
#
#
# @app.callback(
#     Output('chart_bar_runperiod', 'figure'),
#     [Input('input_T', 'value'), Input('input_N', 'value'), Input('input_L', 'value'),
#      Input('input_A', 'value'), Input('input_WB', 'value')]
# )
# def update_graph_runperiod(T_value, N_value, F_value, A_value, W_value):
#     dfi = df_acr_large
#     b = dfi[ (dfi['T'] == T_value) & (dfi.N == N_value) & (dfi.F == F_value) & (dfi.WB == W_value) & (dfi.A == A_value) ].index.tolist()
#     print(b)
#
#     # df_chart_rp = df_acr.loc[b]
#     df_chart_rp = df_acr_large.sort_values(['BD1_TM52_C1'])
#     return {
#         'data': [go.Bar(
#             x = df_chart_rp['BD1_TM52_C1'],
#             y = df_chart_rp.index,
#             orientation='h',
#             marker = dict(color = 'rgba(0,0,0,0.3)'),
#             )],
#         'layout': {
#             'autosize':False,
#             'height': 600,
#             'margin': {'l': 40, 'b': 40, 'r': 40, 't': 60},
#             'xaxis': {'range':[0, 0.8],},
#             'yaxis': {'showticklabels':False,},
#             }
#     }
#
# @app.callback(
#     Output('chart_scatter_runperiod', 'figure'),
#     [Input('input_T', 'value'), Input('input_N', 'value'), Input('input_L', 'value'),
#      Input('input_A', 'value'), Input('WB_value', 'value')]
# )
# def update_graph_runperiod(T_value, N_value, F_value, A_value, WB_value):
#     dfi = df_acr_large
#     b = dfi[(dfi['T'] == T_value) & (dfi.N == N_value) & (dfi.F == F_value) & (dfi.WB == WB_value) & (dfi.A == A_value)].index.tolist()
#     print(b)
#
#     df_chart_rp = df_acr_large.loc[b]
#     marker_size = 100 * df_chart_rp['BD1_TM52_C1']
#     marker_text = str(float((100 * df_chart_rp['BD1_TM52_C1']).round(1))) +'%'
#
#     return {
#         'data': [go.Scatter(
#             x = df_chart_rp.index,
#             y = df_chart_rp['BD1_TM52_C1'],
#             mode='markers+text',
#             marker=dict(size=marker_size),
#             text=marker_text, textposition='auto',
#             )],
#         'layout': {
#             # 'autosize':False,
#             'height': 250,
#             'margin': {'l':20, 'b':40, 'r':20, 't':40},
#             'xaxis': {'showticklabels':False, 'showgrid':False},
#             'yaxis': {'range':[0, 1], 'showgrid':False},
#             'paper_bgcolor':'rgba(0,0,0,0)',
#             'plot_bgcolor':'rgba(0,0,0,0)',
#             }
#     }
#
