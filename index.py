import time
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output, State
from app import app
from app import server
import model

df = pd.read_excel('Data.xlsx')
df.fillna(value='Not Assigned', inplace=True)

header = html.Div([
    html.Div([
        html.H1(["HoTp System"], id='header_name'),
        html.H6("Organizational Log data threat level prediction")
    ], className='header-outer-box'),
], className='header_box')

footer = html.Footer([
    html.P("Copyright 2021. All Rights Reserved.")
], className='footer')

home_content = html.Div([
    html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Label("Enter IP Address", html_for="address"),
                dbc.Input(type='text', id='ip_address', required=True),

                dbc.Label("Enter Threat type", html_for="address"),
                dcc.Dropdown(
                    id='Threat_type_drop',
                    options=[{'label': i, 'value': i} for i in df['Threat type'].unique()],
                    style={'color': 'black'},
                    value=None,
                ),

                dbc.Label("Enter Action Performed", html_for="address"),
                dcc.Dropdown(
                    id='action_Performed_drop',
                    options=[{'label': i, 'value': i} for i in df['Action Performed'].unique()],
                    style={'color': 'black'},
                    value=None,
                ),

                dbc.Label("Enter Action Error", html_for="address"),
                dcc.Dropdown(
                    id='Action_Error_drop',
                    options=[{'label': i, 'value': i} for i in df['Action Error'].unique()],
                    style={'color': 'black'},
                    value=None,
                ),

                dbc.Label("Enter Cirucmstance name", html_for="address"),
                dcc.Dropdown(
                    id='Cirucmstance_name_drop',
                    options=[{'label': i, 'value': i} for i in df['Cirucmstance name'].unique()],
                    style={'color': 'black'},
                    value=None,
                ),

                dbc.Label("Enter Flags", html_for="address"),
                dcc.Dropdown(
                    id='Flags_drop',
                    options=[{'label': i, 'value': i} for i in df['Flags'].unique()],
                    style={'color': 'black'},
                    value=None,
                ),

                dbc.Label("Enter Threat/Content Type", html_for="address"),
                dcc.Dropdown(
                    id='Threat_Content_Type_drop',
                    options=[{'label': i, 'value': i} for i in df['Threat/Content Type'].unique()],
                    style={'color': 'black'},
                    value=None,
                ),

                dbc.Label("Enter TcpTunnel Status", html_for="address"),
                dcc.Dropdown(
                    id='TcpTunnel_Status_drop',
                    options=[{'label': i, 'value': i} for i in df['TcpTunnel Status'].unique()],
                    style={'color': 'black'},
                    value=None,
                ),

                dbc.Label("Enter alertType", html_for="address"),
                dcc.Dropdown(
                    id='alertType_drop',
                    options=[{'label': i, 'value': i} for i in df['alertType'].unique()],
                    style={'color': 'black'},
                    value=None,
                ),
                dbc.Label("Enter Category", html_for="address"),
                dcc.Dropdown(
                    id='Category_drop',
                    options=[{'label': i, 'value': i} for i in df['Category '].unique()],
                    style={'color': 'black'},
                    value=None,
                ),
            ]),
            dbc.Col([
                dbc.Label("Enter Severity occurrence", html_for="address"),
                dcc.Dropdown(
                    id='Severity_occurrence_drop',
                    options=[{'label': i, 'value': i} for i in df['Severity occurance'].unique()],
                    style={'color': 'black'},
                    value=None,
                ),

                dbc.Label("Enter Action", html_for="address"),
                dcc.Dropdown(
                    id='Action_drop',
                    options=[{'label': i, 'value': i} for i in df['Action '].unique()],
                    style={'color': 'black'},
                    value=None,
                ),

                dbc.Label("Enter Session End Reason", html_for="address"),
                dcc.Dropdown(
                    id='Session_End_Reason_drop',
                    options=[{'label': i, 'value': i} for i in df['Session End Reason '].unique()],
                    style={'color': 'black'},
                    value=None,
                ),

                dbc.Label("Enter severity ", html_for="address"),
                dcc.Dropdown(
                    id='severity_drop',
                    options=[{'label': i, 'value': i} for i in df['severity '].unique()],
                    style={'color': 'black'},
                    value=None,
                ),

                dbc.Label("Enter Action  performed", html_for="address"),
                dcc.Dropdown(
                    id='Action_performed_drop',
                    options=[{'label': i, 'value': i} for i in df['Action  performed'].unique()],
                    style={'color': 'black'},
                    value=None,
                ),

                dbc.Label("Enter process name ", html_for="address"),
                dcc.Dropdown(
                    id='process_name_drop',
                    options=[{'label': i, 'value': i} for i in df['process name'].unique()],
                    style={'color': 'black'},
                    value=None,
                ),

                dbc.Label("Enter Mallicious IP", html_for="address"),
                dcc.Dropdown(
                    id='Mallicious_IP_drop',
                    options=[{'label': i, 'value': i} for i in df['Mallicious IP'].unique()],
                    style={'color': 'black'},
                    value=None,
                ),
                dbc.Label("Enter Malware rule", html_for="address"),
                dcc.Dropdown(
                    id='Malware_rule_drop',
                    options=[{'label': i, 'value': i} for i in df['Malware rule '].unique()],
                    style={'color': 'black'},
                    value=None,
                ),
                dbc.Label("Enter main class name", html_for="address"),
                dcc.Dropdown(
                    id='main_class_name_drop',
                    options=[{'label': i, 'value': i} for i in df['main class name'].unique()],
                    style={'color': 'black'},
                    value=None,
                ),
            ]),
        ]),
        html.Center(dbc.Button("Submit", id='button-submit', n_clicks=0, className='btn btn-primary btn-lg')),
        html.Div(id='answer-box', children=[])
    ], className='box')
], className='content-outer-box')

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        header,
        dcc.Loading(type='default', id='loading-1', children=[
            html.Div(id='page_content', children=[]),
        ]),
        footer
    ], className='container'
)


@app.callback(Output('answer-box', 'children'),
              [Input('button-submit', 'n_clicks')],
              [
                  State('ip_address', 'value'),
                  State('Threat_type_drop', 'value'),
                  State('action_Performed_drop', 'value'),
                  State('Action_Error_drop', 'value'),
                  State('Cirucmstance_name_drop', 'value'),
                  State('Flags_drop', 'value'),
                  State('Threat_Content_Type_drop', 'value'),
                  State('TcpTunnel_Status_drop', 'value'),
                  State('alertType_drop', 'value'),
                  State('Category_drop', 'value'),
                  State('Severity_occurrence_drop', 'value'),
                  State('Action_drop', 'value'),
                  State('Session_End_Reason_drop', 'value'),
                  State('severity_drop', 'value'),
                  State('Action_performed_drop', 'value'),
                  State('process_name_drop', 'value'),
                  State('Mallicious_IP_drop', 'value'),
                  State('Malware_rule_drop', 'value'),
                  State('main_class_name_drop', 'value'),
              ]
              )
def get_values(n_click, ip_address, threat_type, action_performed, action_error, cirucmstance_name, flags,
               threat_content_type, tcp_tunnel_status, alert_type, category, severity_occurrence, action,
               session_end_reason, severity, Action_performed, process_name,
               mallicious_ip, malware_rule, main_class_name):
    if n_click > 0:
        if ip_address is None:
            alert = dbc.Alert('Please Fill The IP Address Field And Try Again !', className='alert alert-danger')
        answer = model.model_pred(ip_address, threat_type, action_performed, action_error, cirucmstance_name, flags,
                                  threat_content_type, tcp_tunnel_status, alert_type, category, severity_occurrence,
                                  action, session_end_reason, severity, Action_performed, process_name,
                                  mallicious_ip, malware_rule, main_class_name)
        if answer == 'CRITICAL':
            ans = html.Div([
                html.Div([html.Div([html.Img(src=app.get_asset_url('warning.svg'))], className='blue-anim')],
                         className='red-anim'),
                html.H1(answer),
            ], className='red-answer-inner-box')
        elif answer == 'Low':
            ans = html.Div([
                html.Div([
                    html.Img(src=app.get_asset_url('low_normal.png'))
                ], className='low-anim'),
                html.H1(answer),
            ], className='green-answer-inner-box')
        elif answer == 'NO THREAT':
            ans = html.Div([
                html.Div([html.Img(src=app.get_asset_url('secure-blue.png'))], className='blue-anim'),
                html.H1(answer),
            ], className='blue-answer-inner-box')
        else:
            ans = html.Div([
                html.Div([html.Div([html.Img(src=app.get_asset_url('normal_green.png'))], className='blue-anim')],
                         className='normal-anim'),
                html.H1(answer)
            ], className='answer-inner-box')
        return ans
    else:
        return None


@app.callback(Output(component_id='page_content', component_property='children'),
              Input(component_id='url', component_property='pathname'))
def load_content(pathname):
    if pathname == '/':
        return home_content
    else:
        return ["404 Error"]


if __name__ == "__main__":
    app.run_server(debug=True)
