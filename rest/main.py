from flask import (
    Flask,
    render_template,request,jsonify,Response
)
from flask_cors import CORS
import time
import logging
from DelayMiddleware import Middleware
from flask_executor import Executor
from connections_config import SERVER_PORT,SERVER_HOST
import threading
import io
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
CORS(app)

@app.before_request
def middle():
    middleware.delay(request,executor)

@app.route('/',methods=["POST","GET","PUT","DELETE"])
def home():
    
    if request.method=="POST":
        content = request.get_json(force=True)
        return "post data "+str(content)
    if request.method=="GET":
        return "get method3"
    if request.method=="PUT":
        return "put method"
    if request.method=="DELETE":
        return "delete method"
def func(isim):
    dosya=io.open(isim,"r")
    print("-",dosya.read(),"-")

if __name__ == '__main__':
    #thread=threading.Thread(target=func,args=("requests.log",))
    #thread.start()
    app.run(host=SERVER_HOST,port = SERVER_PORT,debug=False,threaded=True)

