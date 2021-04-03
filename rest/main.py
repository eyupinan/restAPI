from flask import (
    Flask,
    render_template,request,jsonify,Response,g
)
from flask_cors import CORS,cross_origin
import time
import logging
from DelayMiddleware import Middleware
from flask_executor import Executor
import os 
from db_connection import mong
from flask_pymongo import PyMongo
from routes.cities import cities_blueprint
from routes.boroughs import boroughs_blueprint
#os.environ["REST_HOST"]="localhost"
#os.environ["REST_PORT"]="5000"
#os.environ["KAFKA_ADDRESS"]="localhost:9092"
#os.environ["MONGO_ADDRESS"]="localhost:27017"
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
app.config["MONGO_URI"] = "mongodb://"+os.environ["MONGO_ADDRESS"]+"/locations"
mongo = PyMongo(app)
mong_obj=mong(mongo)
CORS(app)
#routes klasörü içerisindeki dosyalar tarafından tanımlanan blueprint'ler flask server'a ekleniyor
cities_print=cities_blueprint(mong_obj).create_blueprint()
boroughs_print=boroughs_blueprint(mong_obj).create_blueprint()
app.register_blueprint(cities_print)
app.register_blueprint(boroughs_print)

@app.before_request
def middle():
    if request.method in ["GET","POST","PUT","DELETE"]:
        print("request received",request.url,request.method)
        g.delay=middleware.delay(request,executor)
        print(g.delay)

#tamamen etkisiz requestlerin atılabilmesi için  kullanılmıştır
@app.route('/',methods=["POST","GET","PUT","DELETE"])
def home():
    if request.method=="POST":
        resp=Response("post method delay:"+str(g.delay),status=200)
    if request.method=="GET":
        resp=Response("get method delay:"+str(g.delay),status=200)
    if request.method=="PUT":
        resp=Response("put method delay:"+str(g.delay),status=200)
    if request.method=="DELETE":
        resp=Response("delete method delay:"+str(g.delay),status=200)
    return resp
if __name__ == '__main__':
    app.run(host=os.environ["REST_HOST"],port = os.environ["REST_PORT"],debug=False,threaded=True)

