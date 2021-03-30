
from werkzeug.wrappers import Request
import logging
import random
import time
from producer import KafkaHandler
import threading
from flask_executor import Executor

FORMAT = '%(method)s,%(delay)s,%(timestamp)s'
producer_log=logging.getLogger("kafka.producer.kafka")
producer_log.setLevel(logging.ERROR)
log = logging.getLogger('kafka.conn')
log.setLevel(logging.ERROR)



class Middleware:

    def __init__(self):
        logging.basicConfig(level=logging.INFO, filename='requests.log',filemode="a")
        self.logKafka = logging.getLogger("restAPI")
        self.logKafka.setLevel(level=logging.INFO)
        kafkahandler=KafkaHandler()
        self.logKafka.addHandler(kafkahandler)
        self.sayac=0
    def random_time(self,req):
        if req.method=="GET":
            delay =random.randint(2400,3000)/1000
        if req.method=="POST":
            delay =random.randint(1900,2400)/1000
        if req.method=="PUT":
            delay =random.randint(1400,1900)/1000
        if req.method=="DELETE":
            delay =random.randint(900,1400)/1000
        
        return delay
    def delay(self,req,executor):
        dl=""
        #content = req.get_json(force=True)
        #print("request received",content["sayac"],req.method,time.time())
        if req.method in ["PUT","GET","POST","DELETE"]:
            dl=self.random_time(req) 
            timestamp=str(int(time.time()))
            time.sleep(dl)
            
            format_map={
            "method":req.method ,     
            "delay":str(int(dl*1000)),
            "timestamp":timestamp
            }
            formatted=FORMAT % format_map
            executor.submit(self.logKafka.info,formatted)
        return dl
