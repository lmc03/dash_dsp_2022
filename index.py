import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output,Input,State
import pandas as pd
import numpy as np
from app import app, server
from apps import dashboard, dashboard2
from dash.exceptions import PreventUpdate
import sqlite3
import bcrypt 
from cryptography.fernet import Fernet

app = dash.Dash(__name__,suppress_callback_exceptions=True)


app.layout = html.Div([
  dcc.Location(id='url', refresh=False),
  html.Div(id='page-content')
                     ])


index_page = html.Div([
    html.Div(
    dcc.Input(id="username", type="text", placeholder="Enter Username",className="inputbox1",
    style={'margin-left':'35%','width':'250px','height':'35px','padding':'10px','margin-top':'200px',
    'font-size':'16px','border-color':'#000000'
    }),
    ),
    html.Div(
    dcc.Input(id="password", type="password", placeholder="Enter Password",className="inputbox2",
    style={'margin-left':'35%','width':'250px','height':'35px','padding':'10px','margin-top':'10px',
    'font-size':'16px','border-color':'#000000',
    }),
    ),
    html.Div(
    html.Button('Login', id='verify', n_clicks=0, style={'font-size':'14px'}),
    style={'margin-left':'43%','padding-top':'30px'}),
    html.Th(id='error-message',style={'textAlign':'Center','color':'rgb(0,123,255)'}),
    html.Div([dcc.Input(id='submitmode', value = 0)
        ], style={'display':'none'})
    ])


@app.callback(
   [Output('url', 'pathname')],
   [Output('submitmode','value')],
   [Input('verify', 'n_clicks')],
   [State('username', 'value'),
    State('password', 'value')])

def update_output(n_clicks, user, password):
    li={'admin':'password'}
    if user not in li:
        return html.Div(children = 'Incorrect Username or Password', style = {'padding top': '20px'})
    if li[user]==password:
        return ['/apps/dashboard',0]
    else:
        return html.Div(children = 'Incorrect Username or Password', style = {'padding top': '20px'})




@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    if pathname == '/apps/dashboard':
        return dashboard.next_page
    else:
        return index_page
   
@app.callback(
    Output('error-message', 'children'),
    [Input('submitmode', 'value')])
def incorrect_input(submit_mode):
    if submit_mode == 1:
        print('incorrect pw')
        return ['Incorrect Username or Password']
    else:
        return [""];
    
@app.callback(
        [Output('tparOutput', 'children'),
         Output('uorOutput', 'children')
         ],
        [Input('submitButton', 'n_clicks')],
        [State('totalHits', 'value'),
         State('revenuePerPurchase', 'value'),
         State('ntpcuy','value'),
         State('conversionRate', 'value')])
def output1(n_clicks, totalHits, revenuePerPurchase, ntpcuy, conversionRate):
    tpar = float(totalHits) * float(revenuePerPurchase) * float(ntpcuy)
    tpar1 = '{:,.2f}'.format(tpar)
    uor = (1 - float(conversionRate)/100) * (float(totalHits) * float(revenuePerPurchase) * float(ntpcuy))
    uor1 = '{:,.2f}'.format(uor)
    return ["Php {}".format(tpar1), "Php {}".format(uor1)]

# Converted Revenue
@app.callback(
        Output('convertedRev', 'children'),
        [Input('submitButton', 'n_clicks')],
        [State('conversionRate', 'value'),
        State('totalHits', 'value'),
        State('revenuePerPurchase', 'value'),
        State('ntpcuy','value')])
def output3(n_clicks, conversionRate, totalHits, revenuePerPurchase, ntpcuy):
    cr = (float(conversionRate)/100) * (float(totalHits) * float(revenuePerPurchase) * float(ntpcuy))
    cr1 = '{:,.2f}'.format(cr)
    return "Php {}".format(cr1)

# Maximum Allowable Spend
@app.callback(
        Output('MaxAllowSpend', 'children'),
        [Input('submitButton', 'n_clicks')],
        [State('conversionRate', 'value'),
        State('totalHits', 'value'),
        State('revenuePerPurchase', 'value'),
        State('ntpcuy','value'),
        State('samplingCost', 'value'),
        State('potentialRevenue', 'value')])
def output4(n_clicks, conversionRate, totalHits, revenuePerPurchase, ntpcuy, samplingCost, potentialRevenue):
    mas = (((float(conversionRate)/100) * (float(totalHits) * float(revenuePerPurchase) * float(ntpcuy))) - float(samplingCost)) * float(potentialRevenue)/100
    mas1 = '{:,.2f}'.format(mas)
    return "Php {}".format(mas1)


# Maximum Allowable Spend Per Hit
@app.callback(
        Output('MaxSpendPerHit', 'children'),
        [Input('submitButton', 'n_clicks')],
        [State('conversionRate', 'value'),
        State('totalHits', 'value'),
        State('revenuePerPurchase', 'value'),
        State('ntpcuy','value'),
        State('samplingCost', 'value'),
        State('potentialRevenue', 'value')])
def output5(n_clicks, conversionRate, totalHits, revenuePerPurchase, ntpcuy, samplingCost, potentialRevenue):
    masph = ((((float(conversionRate)/100) * (float(totalHits) * float(revenuePerPurchase) * float(ntpcuy))) - float(samplingCost)) * float(potentialRevenue)/100)/float(totalHits)
    masph1 = '{:,.2f}'.format(masph)
    return "Php {}".format(masph1)

# Net Profit
@app.callback(
        Output('netProfit', 'children'),
        [Input('submitButton', 'n_clicks')],
        [State('conversionRate', 'value'),
        State('totalHits', 'value'),
        State('revenuePerPurchase', 'value'),
        State('ntpcuy','value'),
        State('samplingCost', 'value')])
def output6(n_clicks, conversionRate, totalHits, revenuePerPurchase, ntpcuy, samplingCost):
    np = ((float(conversionRate)/100) * (float(totalHits) * float(revenuePerPurchase) * float(ntpcuy))) - float(samplingCost)
    np1 = '{:,.2f}'.format(np)
    return "Php {}".format(np1)

# For Waterfall Chart
@app.callback(
        Output('waterfall', 'figure'),
        [Input('submitButton', 'n_clicks')],
        [State('conversionRate', 'value'),
        State('totalHits', 'value'),
        State('revenuePerPurchase', 'value'),
        State('ntpcuy','value'),
        State('samplingCost', 'value'),
        State('potentialRevenue', 'value')])
def waterfall(n_clicks, conversionRate, totalHits, revenuePerPurchase, ntpcuy, samplingCost, potentialRevenue):
    tpar = float(totalHits) * float(revenuePerPurchase) * float(ntpcuy)
    uor = np.abs((1 - float(conversionRate)/100) * tpar)
    convertedRev = (float(conversionRate)/100) * tpar
    netProfit = convertedRev - float(samplingCost)
    netProfitNFS = np.abs((1 - float(potentialRevenue)/100) * netProfit)
    MaxAllowSpend = (float(potentialRevenue)/100) * netProfit

    fig = {
            'data': [
                    {'labels':['tpar','uor'],
                     'x':['Total Potential Annual Revenue', 'Unconverted Opportunity Revenue'],
                     'y':[tpar,-uor],
                     'type':'waterfall',
                     'increasing':{'marker':{'color':'rgba(44, 82, 103, 0.70)'}},
                     'decreasing':{'marker':{'color':'rgba(255, 59, 60, 0.70)'}},
                     'connector': {'visible':False}},
                     {'labels':['tcs','uor'],
                      'x':['Converted Revenue', 'Sampling Cost'],
                      'y':[convertedRev,-float(samplingCost)],
                      'type':'waterfall',
                      'increasing':{'marker':{'color':'rgba(44, 82, 103, 0.70)'}},
                     'decreasing':{'marker':{'color':'rgba(255, 59, 60, 0.70)'}},
                     'connector': {'visible':False}},
                    {'labels':['tcs','uor'],
                     'x':['Net Profit', 'Net Profit Not For Sampling'],
                     'y':[netProfit,-netProfitNFS],
                     'type':'waterfall',
                     'increasing':{'marker':{'color':'rgba(44, 82, 103, 0.70)'}},
                     'decreasing':{'marker':{'color':'rgba(255, 59, 60, 0.70)'}},
                     'connector': {'visible':False}},
                    {'labels':['tcs'],
                     'x':['Max Allowable Spend'],
                     'y':[MaxAllowSpend],
                     'type':'waterfall',
                     'increasing':{'marker':{'color':'rgba(44, 82, 103, 0.70)'}},
                     'decreasing':{'marker':{'color':'rgba(255, 59, 60, 0.70)'}},
                     'connector': {'visible':False}}
                    ],
    'layout': {'showlegend': False,
               'xaxis':{'automargin':True, 'title':'ROI Parameters'},
               'margin':dict(t = 0)
            }}
    return fig

@app.callback(
         Output('donut', 'figure'),
         [Input('submitButton', 'n_clicks')],
         [State('conversionRate', 'value'),
          State('totalHits', 'value'),
          State('revenuePerPurchase', 'value'),
          State('ntpcuy','value'),
          State('samplingCost', 'value'),
          State('potentialRevenue', 'value')])
def donutchart(n_clicks, conversionRate, totalHits, revenuePerPurchase, ntpcuy, samplingCost, potentialRevenue):
    tpar = float(totalHits) * float(revenuePerPurchase) * float(ntpcuy)
    uor = (1 - float(conversionRate)/100) * tpar
    convertedRev = (float(conversionRate)/100) * tpar
    netProfit = convertedRev - float(samplingCost)
    netProfitNFS = (1 - float(potentialRevenue)/100) * netProfit
    MaxAllowSpend = (float(potentialRevenue)/100) * netProfit
    a = ['Unconverted Revenue', 'Sampling Cost', 'Max Allowable Spend', 'Net Profit Not For Sampling']
    b = [uor, samplingCost, MaxAllowSpend, netProfitNFS]

    fig = { "data": [
    {
      "values": b,
      "labels": a,
      "marker": {
              'colors':['rgb(242, 217, 187)',
              'rgb(44,82,103)',
              'rgb(134, 169, 189)',
              'rgb(255, 59, 60)'],
                'line':{'colors':['rgba(1,1,1,0)'], 'width': 2}
              },
      "hoverinfo":"label+percent",
      "hole": .4,
      "type": "pie",
      'textposition':'outside',
      'outsidetextfont':{"size":11},
      "textinfo":"label+value"
    }],
    'layout': {#'title': 'Investment or Income Breakdown',
               'showlegend': False,
               'margin':dict(t = 0)},
            'config':{
                    'displayModeBar':False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
}
    return fig



@app.callback(
         [Output('ddselectscenario', 'options'),
          Output('ddselectscenario', 'value'),
          ],
         [
             Input('saveButton', 'n_clicks'),
             Input('mode','value'),
             Input('deleteButton', 'n_clicks'),
             ],
         [
          State('scenarioname', 'value'),  
          State('conversionRate', 'value'),
          State('totalHits', 'value'),
          State('revenuePerPurchase', 'value'),
          State('ntpcuy','value'),
          State('samplingCost', 'value'),
          State('potentialRevenue', 'value'),
          State('ddselectscenario', 'value'),
          ])
def savescenarios(n_clicks,mode,deleteButton,scenarioname, conversionRate, totalHits, revenuePerPurchase,
                  ntpcuy, samplingCost, potentialRevenue,ddselectscenario):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="saveButton":
            if 1 not in mode:
                sql = "SELECT max(scenario_id) as scenario_id FROM scenario_names"
                df = querydatafromdatabase(sql,[],["scenario_id"])
           
                if not df['scenario_id'][0]:
                    scenario_id=1
                else:
                    scenario_id = int(df['scenario_id'][0])+1
                sqlinsert = '''INSERT INTO
                scenario_names(scenario_id,scenario_name,totalhits,
                               conversionrate, revenueperpurchase,
                               npurchaseperyear, costofsampling,
                               percentrevenue) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
                modifydatabase(sqlinsert, (scenario_id,scenarioname,totalHits,conversionRate,revenuePerPurchase,
                                          ntpcuy,samplingCost,potentialRevenue  ))
            else:
                sqlinsert = '''UPDATE scenario_names SET scenario_name= ?,totalhits= ?,
                               conversionrate= ?, revenueperpurchase= ?,
                               npurchaseperyear= ?, costofsampling= ?,
                               percentrevenue = ? WHERE scenario_id = ?'''
                modifydatabase(sqlinsert, (scenarioname,totalHits,conversionRate,revenuePerPurchase,
                                          ntpcuy,samplingCost,potentialRevenue,ddselectscenario  ))          
       elif eventid =="deleteButton":
            sqlinsert = '''DELETE FROM scenario_names WHERE scenario_id = ?'''
            modifydatabase(sqlinsert, (ddselectscenario,))
       sql = "SELECT scenario_name, scenario_id FROM scenario_names"
       df = querydatafromdatabase(sql,[],["label","value"])
       return [df.to_dict('records'),df.to_dict('records')[0]['value']]
   else:
       sql = "SELECT scenario_name, scenario_id FROM scenario_names"
       df = querydatafromdatabase(sql,[],["label","value"])
       return [df.to_dict('records'),df.to_dict('records')[0]['value']]

@app.callback(
         [
          Output('scenarioname', 'value'),  
          Output('conversionRate', 'value'),
          Output('totalHits', 'value'),
          Output('revenuePerPurchase', 'value'),
          Output('ntpcuy','value'),
          Output('samplingCost', 'value'),
          Output('potentialRevenue', 'value')
         
          ],
         [
             Input('ddselectscenario', 'value')],
         [
          ])
def loadcenarios(ddselectscenario):
    if ddselectscenario:
        sql = "SELECT * FROM scenario_names WHERE scenario_id=?"
        df = querydatafromdatabase(sql,[ddselectscenario],["scenario_id","scenario_name",'totalhits',
                                           "conversionrate","revenueperpurchase","npurchaseperyear","costofsampling","percentrevenue"])
       
        scenario_name = df["scenario_name"][0]
        totalhits = df["totalhits"][0]
        conversionrate = df["conversionrate"][0]
        revenueperpurchase = df["revenueperpurchase"][0]
        npurchaseperyear = df["npurchaseperyear"][0]
        costofsampling = df["costofsampling"][0]
        percentrevenue = df["percentrevenue"][0]
        return [scenario_name,conversionrate,totalhits,revenueperpurchase,npurchaseperyear,costofsampling,percentrevenue ]
    else:
        raise PreventUpdate

def querydatafromdatabase(sql, values,dbcolumns):
    db = sqlite3.connect('scenarios.db')
    cur = db.cursor()
    cur.execute(sql, values)
    rows = pd.DataFrame(cur.fetchall(), columns=dbcolumns)
    db.close()
    return rows

def modifydatabase(sqlcommand, values):
    db = sqlite3.connect('scenarios.db')
    cursor = db.cursor()
    cursor.execute(sqlcommand, values)
    db.commit()
    db.close()

if __name__=='__main__':
    app.run_server()