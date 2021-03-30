from flask import (
    Flask,
    render_template,request,jsonify,Response,g
)
from flask_cors import CORS,cross_origin
import time
import logging
from DelayMiddleware import Middleware
from flask_executor import Executor
import threading
import io
import os 
from db_connection import mong
os.environ["REST_HOST"]="localhost"
os.environ["REST_PORT"]="5000"
os.environ["KAFKA_ADDRESS"]="localhost:9092"
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

log = logging.getLogger('kafka.conn')
log.setLevel(logging.ERROR)

#middleware objesi 0 ile 3 saniye arasında bir delay koyar.
#ardından bir log dosyasına bilgi yazar ve kafka'ya mesaj gönderir.
#kafkaya gönderilen mesaj ve log dosyasına yazma işlemler Executor ile async bir şekilde gerçekleştirilir.
middleware=Middleware()
mong_obj=mong()
app = Flask(__name__, template_folder="templates")
executor = Executor(app)
CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'
def get_content(req):
    try:
        content = req.get_json(force=True)
    except:
        content={}
    return content
        
@app.before_request
def middle():
    print("request received",request.url,request.method)
    if request.method in ["GET","POST","PUT","DELETE"]:
        g.delay=middleware.delay(request,executor)
        print(g.delay)

@app.route('/',methods=["POST","GET","PUT","DELETE"])
def home():
    print(request.url)
    if request.method=="POST":
        resp=Response("post method delay:"+str(g.delay),status=200)
    if request.method=="GET":
        resp=Response("get method delay:"+str(g.delay),status=200)
    if request.method=="PUT":
        resp=Response("put method delay:"+str(g.delay),status=200)
    if request.method=="DELETE":
        resp=Response("delete method delay:"+str(g.delay),status=200)
    content = request.get_json(force=True)
    print("delay bitti",content["sayac"],g.delay,time.time())
    return resp
@app.route('/<city_name>',methods=["POST","GET","PUT","DELETE"])
@app.route('/city',methods=["POST","GET","PUT","DELETE"])
@app.route('/city/<city_name>',methods=["POST","GET","PUT","DELETE"])
def set_city(city_name=None):
    if request.method=="POST":
        content = request.get_json(force=True)
        if city_name!=None:
            content["name"]=city_name
        mong_obj.setCity(content)
    elif request.method=="GET":
        result_arr=mong_obj.getCity(request.args,city_name=city_name)
        response_json={"cities":result_arr}
        js=jsonify(response_json)
        return js
    elif request.method=="PUT":
        if bool(request.args)!=False or city_name!=None:
            content=get_content(request)
            mong_obj.updateCity(request.args,content,city_name)
            return Response("başarılı",status=200)
        else:
            return Response("sorgu bulunamadi!",status=500)
    elif request.method=="DELETE":
        content=get_content(request)
        mong_obj.deleteCity(content,city_name=city_name)
        return Response("başarılı",status=200)

    
        
@app.route('/<city_name>/<name>',methods=["POST","GET"])
@app.route('/<city_name>/borough',methods=["POST","GET"])
@app.route('/borough/<name>',methods=["POST","GET"])
@app.route('/borough',methods=["POST","GET"])
def set_borough_with_city_name(city_name=None,name=None):
    if request.method=="POST":
        content = request.get_json(force=True)
        if name!=None:
            content["name"]=name
        if city_name==None:
            city_name=content["city_name"]
        mong_obj.setBorough(content,city_name)
    elif request.method=="GET":
        content = request.args
        result=mong_obj.getBorough(content,city_name,name)
        result_json={"boroughs":result}
        js=jsonify(result_json)
        return js
    elif request.method=="PUT":
        if bool(request.args)!=False or name!=None:
            content=get_content(request)
            mong_obj.updateBorough(request.args,content,city_name,name)
        else:
            return Response("sorgu bulunamadı",status=400)
    elif request.method=="DELETE":
        content=get_content(request)
        mong_obj.deleteBorough(content,city_name=city_name,name=name)
        return Response("başarılı",status=200)



if __name__ == '__main__':
    app.run(host=os.environ["REST_HOST"],port = os.environ["REST_PORT"],debug=False,threaded=True)

