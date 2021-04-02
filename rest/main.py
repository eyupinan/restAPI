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
from flask_pymongo import PyMongo
from routes.cities import cities_blueprint
from routes.boroughs import boroughs_blueprint
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

app = Flask(__name__, template_folder="templates")
executor = Executor(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/locations"
mongo = PyMongo(app)
mong_obj=mong(mongo)
CORS(app)
#routes klasörü içerisindeki dosyalar tarafından tanımlanan blueprint'ler flask server'a eklenir
cities_print=cities_blueprint(mong_obj).create_blueprint()
boroughs_print=boroughs_blueprint(mong_obj).create_blueprint()
app.register_blueprint(cities_print)
app.register_blueprint(boroughs_print)
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
    
    if request.method in ["GET","POST","PUT","DELETE"]:
        print("request received",request.url,request.method)
        g.delay=middleware.delay(request,executor)
        print(g.delay)

#tamamen etkisiz requestlerin atılabilmesi için  kullanılmıştır
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
    return resp
@app.route('/city/<city_name>/update',methods=["PUT"])
@app.route('/<city_name>/update',methods=["PUT"])
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

