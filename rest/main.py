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
def add_value(args,entity_name_list,value_list):
    for index in range(len(entity_name_list)):
        if value_list[index]!=None:
            args[entity_name_list[index]]=value_list[index]
    return args

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
        content=get_content(request)
        args_dict=request.args.to_dict()
        content=add_value(content,["name"],[city_name])
        mong_obj.setCity(args_dict,content)

    elif request.method=="GET":
        args_dict=request.args.to_dict()
        args_dict=add_value(args_dict,["name"],[city_name])
        result_arr=mong_obj.getCity(args_dict)
        response_json={"cities":result_arr}
        js=jsonify(response_json)
        return js
    elif request.method=="PUT":
        if bool(request.args)!=False or city_name!=None:
            content=get_content(request)
            args_dict=add_value(request.args.to_dict(),["name"],[city_name])
            state=mong_obj.updateCity(args_dict,content)
            if state==True:
                return Response("başarılı",status=200)
            else:
                return Response("başarısız",status=400)
        else:
            return Response("sorgu bulunamadi!",status=400)
    elif request.method=="DELETE":
        content=add_value(get_content(request),["name"],[city_name])
        state=mong_obj.deleteCity(content)
        if state==True:
            return Response("başarılı",status=200)

    
@app.route('/<city_name>/<borough_name>',methods=["POST","GET","PUT","DELETE"])
@app.route('/<city_name>/borough',methods=["POST","GET","PUT","DELETE"])
@app.route('/borough/<borough_name>',methods=["POST","GET","PUT","DELETE"])
@app.route('/borough',methods=["POST","GET","PUT","DELETE"])
def set_borough_with_city_name(city_name=None,borough_name=None):
    ref={"name":city_name}# referans eklemek için parametre olarak verilir
    #ismi verilmiş olan şehrin id değeri yapılacak işleme dahil edilir
    if request.method=="POST":
        content=add_value(get_content(request),["name"],[borough_name])
        args_dict=request.args.to_dict()
        mong_obj.setBorough(args_dict,content,ref)
    elif request.method=="GET":
        args_dict=add_value(request.args,["name"],[borough_name])
        result=mong_obj.getBorough(args_dict,ref)
        result_json={"boroughs":result}
        js=jsonify(result_json)
        return js
    elif request.method=="PUT":
        if bool(request.args)!=False or borough_name!=None:
            content=get_content(request)
            args_dict=add_value(request.args.to_dict(),["name"],[borough_name])
            
            mong_obj.updateBorough(args_dict,content,ref)
        else:
            return Response("sorgu bulunamadı",status=400)
    elif request.method=="DELETE":
        content=add_value(get_content(request),["name"],[borough_name])
        mong_obj.deleteBorough(content,ref)
        return Response("başarılı",status=200)
@app.route('/city/<city_name>/update',methods=["PUT"])
@app.route('/city/<city_name>/update/<entity_name>/<value>',methods=["PUT"])
@app.route('/<city_name>/update/<entity_name>/<value>',methods=["PUT"])
def update_city(city_name,entity_name=None,value=None):
    if bool(request.args)!=False or (entity_name!=None and value!=None):# bir update datasının sağlandığının kontrolü
        #bu kullanımda city_name url kısmı sorgu için update sonrasında verilecek entity ismi ile verilen
        #parametre  veya query parametreleri update edilecek data olarak kullanılır.
        content=request.args.to_dict()
        content=add_value(content,[entity_name],[value])
        query={"name":city_name}
        mong_obj.updateCity(query,content)
        return Response("başarılı",status=200)
    else:
        return Response("gerekli parametreler sağlanmadı",status=400)
@app.route('/borough/<borough_name>/update',methods=["PUT"])
@app.route('/<city_name>/<borough_name>/update',methods=["PUT"])
@app.route('/<city_name>/<borough_name>/update/<entity_name>/<value>',methods=["PUT"])
@app.route('/borough/<borough_name>/update/<entity_name>/<value>',methods=["PUT"])
def update_borough(borough_name,entity_name,value,city_name=None):
    if bool(request.args)!=False or (entity_name!=None and value!=None):# bir update datasının sağlandığının kontrolü
        #burada url içerisindeki ilçe ismi ve şehir ismi sorgu için , update dizini sonrasındaki url parametreleri
        # ve query parametreleri update datası olarak kullanılmıştır
        content=request.args.to_dict()
        content=add_value(content,[entity_name],[value])
        query={"name":borough_name}
        ref={"name":city_name}
        mong_obj.updateBorough(query,content,ref)
        return Response("başarılı",status=200)
    else:
        return Response("gerekli parametreler sağlanmadı",status=400)


if __name__ == '__main__':
    app.run(host=os.environ["REST_HOST"],port = os.environ["REST_PORT"],debug=False,threaded=True)

