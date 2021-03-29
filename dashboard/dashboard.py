import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import pymongo
import time
import pandas as pd
import numpy as np
from datetime import datetime
import os 
import logging
from dateutil import tz
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
myclient = pymongo.MongoClient("mongodb://"+os.environ["MONGO_ADDRESS"])
#myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["mydatabase4"]
mycol = mydb["mylogs"]
ist=tz.gettz("Turkey/Istanbul")
def get_arr(mycol,method):
        now = time.time()
        #print("now:",now)
        #print(datetime.fromtimestamp(now).strftime('%H:%M:%S'))
        query = { "method": method , "timestamp": { "$gt" : now-3600 }}
        logs = mycol.find(query)
        arr1=[]
        arr2=[]
        date_time=[]
        for i in logs:
            #ek=int(i["timestamp"])%60
            tmstp=int(i["timestamp"])-(now-3600)
            date_time.append(pd.to_datetime(datetime.fromtimestamp(i["timestamp"],tz=ist).strftime('%H:%M:%S')))
            arr1.append(tmstp)
            arr2.append(float(i["delay"]))
        date_time = pd.to_datetime(date_time)
        DF = pd.DataFrame()
        DF['delay'] = arr2
        DF = DF.set_index(date_time)
        return DF
def trace_generator(mycol):
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    getDF=get_arr(mycol,"GET")
    postDF=get_arr(mycol,"POST")
    putDF=get_arr(mycol,"PUT")
    delDF=get_arr(mycol,"DELETE")
    aralik="10S"
    #print(getDF)
    getDF=getDF.resample(aralik).mean().fillna(method='ffill')
    #print("---")
    #print(getDF)
    #exit()
    postDF=postDF.resample(aralik).mean().fillna(method='ffill')
    putDF=putDF.resample(aralik).mean().fillna(method='ffill')
    delDF=delDF.resample(aralik).mean().fillna(method='ffill')
    get_trace = plotly.graph_objs.Scatter(
        x=getDF.index,
        y=getDF["delay"],
        name='get method',
        mode='lines',
        line=dict(
            shape='hv',
            width=1
        )
    )
    
    post_trace = plotly.graph_objs.Scatter(
        x=postDF.index,
        y=postDF["delay"],
        name='post method',
        mode='lines',
        line=dict(
            shape='hv',
            width=1
        )
    )
    put_trace = plotly.graph_objs.Scatter(
        x=putDF.index,
        y=putDF["delay"],
        name='put method',
        mode='lines',
        line=dict(
            shape='hv',
            width=1
        )
    )
    del_trace = plotly.graph_objs.Scatter(
        x=delDF.index,
        y=delDF["delay"],
        name='delete method',
        mode='lines',
        line=dict(
            shape='hv',
            width=1
        )
    )
    return [get_trace,post_trace,put_trace,del_trace]
traces=trace_generator(mycol)
now=time.time()
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    '/assets/dashboard.css'
]
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
        html.H4(id="header",children='restAPI Response Delay Dashboard'),
        dcc.Graph(id='live-graph'),
        dcc.Interval(
            id='graph-update',
            interval=1*5000
        ),
    ],id="layout"
)


@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_scatter(n):
    traces=trace_generator(mycol)
    print(traces[0].x)
    now=time.time()
    print(datetime.fromtimestamp(now),tz=ist)
    datetime.fromtimestamp(now)
    return {'data': traces,
            'layout': go.Layout(
                xaxis=dict(range=[datetime.fromtimestamp(now-3600,tz=ist),datetime.fromtimestamp(now,tz=ist)]),
                yaxis=dict(range=[0, 3000]),
                plot_bgcolor='#eeebeb',
                paper_bgcolor='#eeebeb',
                height=640)
            }


if __name__ == '__main__':
    app.run_server(host="0.0.0.0",port=8052, debug=False)
