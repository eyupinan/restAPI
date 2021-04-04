import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import pymongo
import time
import pandas as pd
from datetime import datetime
import os 
import logging
from dateutil import tz
ist=tz.gettz("Europe/Istanbul")
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
pd.set_option("display.max_rows", None, "display.max_columns", None)
while True:
    try:
        myclient = pymongo.MongoClient("mongodb://"+os.environ["MONGO_ADDRESS"])
        mydb = myclient["kafkaLogs"]
        mycol = mydb["mylogs"]
        break
    except:
        logging.info("database bağlantısı kurulamadı 1 saniye sonra tekrar denenecek")
        time.sleep(1)



def get_arr(mycol,method):
        #database üzerine sorgu yapılıyor ve elde edilen veriler bir pandas dataFrame i içerisine yerleştiriliyor
        now = time.time()
        query = { "method": method , "timestamp": { "$gt" : now-3600 }}
        logs = mycol.find(query)
        
        delay_arr=[]
        date_time=[]
        for i in logs:
            date_time.append(pd.to_datetime(datetime.fromtimestamp(i["timestamp"],tz=ist)))
            delay_arr.append(float(i["delay"]))
        date_time = pd.to_datetime(date_time)
        DF = pd.DataFrame()
        DF['delay'] = delay_arr
        DF = DF.set_index(date_time)
        return DF
def trace_generator(mycol):
    #plotly için dataFrameleri oluşturuluyor ve bu frame'lerden her bir method için trace oluşturuluyor.    
    getDF=get_arr(mycol,"GET")
    postDF=get_arr(mycol,"POST")
    putDF=get_arr(mycol,"PUT")
    delDF=get_arr(mycol,"DELETE")
    aralik="10S"
    getDF=getDF.resample(aralik).mean().fillna(method='ffill')
    postDF=postDF.resample(aralik).mean().fillna(method='ffill')
    putDF=putDF.resample(aralik).mean().fillna(method='ffill')
    delDF=delDF.resample(aralik).mean().fillna(method='ffill')
    fill_type="tozeroy"
    get_trace = plotly.graph_objs.Scatter(
        x=getDF.index,
        y=getDF["delay"],
        name='get method',
        mode='lines',
        fill=fill_type,
        fillcolor="rgba(0, 0, 255, 0.1)",
        line=dict(
            shape='hv',
            width=1,
            color="rgb(0, 0, 255)"
        )
    )
    
    post_trace = plotly.graph_objs.Scatter(
        x=postDF.index,
        y=postDF["delay"],
        name='post method',
        mode='lines',
        fill=fill_type,
        fillcolor="rgba(255, 0, 0, 0.1)",
        line=dict(
            shape='hv',
            width=1,
            color="rgb(255, 0, 0)"
        )
    )
    put_trace = plotly.graph_objs.Scatter(
        x=putDF.index,
        y=putDF["delay"],
        name='put method',
        mode='lines',
        fill=fill_type,
        fillcolor="rgba(0, 118, 0, 0.1)",
        line=dict(
            shape='hv',
            width=1,
            color="rgb(0, 118, 0)"
        )
    )
    del_trace = plotly.graph_objs.Scatter(
        x=delDF.index,
        y=delDF["delay"],
        name='delete method',
        mode='lines',
        fill=fill_type,
        fillcolor="rgba(214, 60, 170, 0.1)",
        line=dict(
            shape='hv',
            width=1,
            color="rgb(214, 60, 170)"
        )
    )
    return [get_trace,post_trace,put_trace,del_trace]

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
    #belirli bir zaman aralığı ile dashboard'ın güncelleme işlemi gerçekleştiriliyor.
    traces=trace_generator(mycol)
    now=time.time()
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
