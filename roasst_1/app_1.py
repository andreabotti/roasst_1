import os

import dash
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash(__name__)
server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([
    html.H2('Sample app by Andrea'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['Roma', 'Milano', 'Modena']],
        value='LA'
    ),
    html.Div(id='display-value')
])


@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)