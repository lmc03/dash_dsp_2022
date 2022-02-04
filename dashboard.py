import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import base64
import numpy as np
import sqlite3
from app import app
from dash.exceptions import PreventUpdate
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

next_page = html.Div([
html.Div(dcc.Link('Log out', href='/',style={'color':'#000000','font-family': 'serif', 'font-weight': 'bold', "text-decoration": "none",'font-size':'20px'}),style={'padding-left':'90%','padding-top':'10px'}),
        html.Div(style = {'background-color':'rgb(0,123,255)', 'width':'100%', 'height':40}),
        html.Div([
                html.Div([
                        html.H2("Return of Investments Inputs:", style = {'color':'rgb(0,123,255)', 'font':'Verdana'}),
                        html.Table([
                                html.Tr(children = [html.Td("Scenario Name:", className='lined', style={'width': '50%'}),
                                                    html.Td(dcc.Input(id = 'scenarioname', type='text', value = 'Scenario 1', style = {'fontSize': 20}))]),                            
                                html.Tr(children = [html.Td("Total Hits:", className='lined', style={'width': '50%'}),
                                                    html.Td(dcc.Input(id = 'totalHits', type='number', value = 1000000, style = {'fontSize': 20}))]),
                               
                                html.Tr(children = [html.Td("Conversion Rate:", className='lined', style={'width': '50%'}),
                                                    html.Td(dcc.Input(id = 'conversionRate', type='number', value = 60, style = {'fontSize': 20})
                                                            )]),
                                html.Tr(children = [html.Td("Revenue Per Purchase (PhP):", className='lined', style={'width': '50%'}),
                                                    html.Td(dcc.Input(id = 'revenuePerPurchase', type='number', value = 50, style = {'fontSize': 20})
                                                            )]),
                                html.Tr(children = [html.Td("Number of Times of Purchase per Converted User per Year:", className='lined', style={'width': '50%'}),
                                                    html.Td(dcc.Input(id = 'ntpcuy', type='number', value = 2, style = {'fontSize': 20})
                                                            )]),
                                html.Tr(children = [html.Td("Total Cost of Sampling (PhP):", className='lined', style={'width': '50%'}),
                                                    html.Td(dcc.Input(id = 'samplingCost', type='number', value = 25000000, style = {'fontSize': 20})
                                                            )]),
                                html.Tr(children = [html.Td("% of Potential Revenue You are willing to allocate for sampling", className='lined', style={'width': '50%'}),
                                                    html.Td(dcc.Input(id = 'potentialRevenue', type='number', value = 50, style = {'fontSize': 20})
                                                            )]),
                        ], style = {'width':'100%'}),
                        html.Hr(),
                        html.Button(id = 'submitButton',
                            children = 'Calculate ROI',
                            n_clicks = 0, className='btn btn-primary btn',
                            style = {'fontSize': '15px', 'color':'white', 'background-color':'rgb(0,123,255)', 'float':'middle', 'border-radius':'5px', 'border':'5px'}
                            ),
                        html.Hr(),
                        html.Table([        
                            html.Tr([
                                html.Td([
                                    "Select Scenario:"
                                    ], style={'width': '50%'}),
                                html.Td([
                                    dcc.Dropdown( id = "ddselectscenario")
                                    ], style={'width': '50%'})                                
                                ]),
                            html.Tr([                            
                                 html.Td([
                                    html.Button(id = 'saveButton',
                                        children = 'Save Settings',
                                        n_clicks = 0, className='btn btn-primary btn',
                                        style = {'fontSize': '15px', 'color':'white', 'background-color':'rgb(0,123,255)', 'float':'middle', 'border-radius':'5px', 'border':'5px'}
                                        ),
                                ]),
                                html.Td([
                                    dcc.Checklist(
                                        options=[
                                            {'label': 'Edit Mode', 'value': 1},
                                        ],
                                        id="mode",
                                        value=[],
                                        labelStyle={'display': 'inline-block'}
                                    )
                                                                     
                                ]),
                            ]),
                            html.Tr([
                                 html.Td([
                                    html.Button(id = 'deleteButton',
                                        children = 'Delete This Scenario',
                                        n_clicks = 0, className='btn btn-primary btn',
                                        style = {'fontSize': '15px', 'color':'white', 'background-color':'rgb(0,123,255)', 'float':'middle', 'border-radius':'5px', 'border':'5px'}
                                        ),
                                     
                                ])                                
                             ]),
                        ], style = {'width':'100%'}),
                               
                ], style = {'width':'30%', 'display':'inline-block', 'float':'left', 'marginTop':'0px'}),

                html.Div([
                        html.H2(children='Investment/Income Breakdown:', style = {'textAlign':'center', 'color':'rgb(0,123,255)', 'font':'Verdana'}),
                        dcc.Graph(id = 'donut', style = {'height':300}, config = {
                                          'displayModeBar':False,
                                          'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}),
                        html.H2(children='ROI Parameters Computed:', style = {'color':'rgb(0,123,255)', 'font':'Verdana', 'textAlign':'center'}),
                        html.Table([
                                html.Tr(children = [html.Td("Total Potential Annual Revenue",
                                                className='lined', style={'width': 150, 'border':'1px solid black', 'fontSize':15}),
                                                html.Td(html.Div(id = 'tparOutput', style = {'float':'right'}),
                                                className='lined', style={'width': 200, 'border':'1px solid black'})
                                        ], style = {'height':'10%'}),
                                html.Tr(children = [html.Td("Unconverted Opportunity Revenue",
                                                        className='lined', style={'width': 150, 'border':'1px solid black'}),
                                                html.Td(html.Div(id = 'uorOutput', style = {'float':'right'}),
                                                        className='lined', style={'width': 200, 'border':'1px solid black'})
                                                ]),
                                html.Tr(children = [html.Td("Converted Revenue",
                                                        className='lined', style={'width': 150, 'border':'1px solid black'}),
                                                html.Td(html.Div(id = 'convertedRev', style = {'float':'right'})
                                                        , className='lined', style={'width': 200, 'border':'1px solid black'})
                                                ]),
                                html.Tr(children = [html.Td("Maximum Allowable Spend",
                                                        className='lined', style={'width': 150, 'border':'1px solid black'}),
                                                html.Td(html.Div(id = 'MaxAllowSpend', style = {'float':'right'})
                                                        , className='lined', style={'width': 200, 'border':'1px solid black'})
                                                ]),
                                html.Tr(children = [html.Td("Maximum Spend per Hit",
                                                        className='lined', style={'width': '60%', 'border':'1px solid black'}),
                                                html.Td(html.Div(id = 'MaxSpendPerHit', style = {'float':'right'})
                                                        , className='lined', style={'width': '40%', 'border':'1px solid black'})
                                                ])
                                    ], style = {'border-collapse':'collapse', 'width':'100%'}),
                        html.H2(children = "Estimated Net Profit From Sampling:", style = {'color':'rgb(0,123,255)', 'font':'Verdana', 'textAlign':'center'}),
                        html.Table([
                                html.Tr(children = [html.Td("Net Profit",
                                                className='lined', style={'width': '30%', 'border':'1px solid black'}),
                                        html.Td(html.Div(id = 'netProfit', style = {'float':'right'})
                                                , className='lined', style={'width': '70%', 'border':'1px solid black'})
                                        ])
                                ], style ={'border-collapse':'collapse', 'width':'100%'})
                ], className='cmd', style = {'width':'35%', 'display':'inline-block','float':'left'}),

                html.Div([
                        html.H2("Waterfall Chart", style = {'textAlign':'center', 'color':'rgb(0,123,255)', 'font':'Verdana', 'height':'10vh'}),
                        dcc.Graph(id = 'waterfall',
                                  config = {
                                          'displayModeBar':False,
                                          'modeBarButtonsToRemove': ['pan2d', 'lasso2d']})
                ], style = {'width':'35%', 'display':'inline-block', 'float':'right'})
            ])
        ])

#make sure to place all callbacks into index.py since the returns do not work properly in dashboad.py
       

if __name__ == '__main__':
    app.run_server()
