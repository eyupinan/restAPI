from kafka import KafkaConsumer
import pymongo
import logging
import time
import os
import json
log = logging.getLogger('kafka.conn')
log.setLevel(logging.CRITICAL)
class listener:
    def __init__(self,mongo_address,kafka_adress,kafka_topic):
        self.set_validate_function(lambda msg : None)
        while True:
            try:
                self.consumer = KafkaConsumer(kafka_topic,bootstrap_servers=kafka_adress,
                                            value_deserializer=lambda m: json.loads(m.decode('utf-8')))
                self.myclient = pymongo.MongoClient("mongodb://"+mongo_address)
                self.mydb = self.myclient["mydatabase4"]
                self.mycol = self.mydb["mylogs"]
                break
            except Exception as e:
                logging.warning("bağlantı kurulamadı:"+str(e))
                time.sleep(1)    
 
    def set_validate_function(self,func):
        self.validate=func
    def listen(self):
        for msg in self.consumer:
            try:
                
                self.validate(msg.value)
                x = self.mycol.insert_one(msg.value)
                if (x.acknowledged==False):
                    raise Exception("mesaj veritabanına yazılamadı!")
            except Exception as e:
                logging.error("log hatası: "+str(e))
def validate(msg):
        if type(msg)!=dict:
            raise Exception("message type is not valid")
        if msg["method"] not in ["GET","POST","PUT","DELETE"]:
            raise Exception("method is not valid")
        if not msg["delay"].isdigit():
            raise Exception("delay is not valid")
        if type(msg["timestamp"])!=int:
            raise Exception("timestamp is not valid")
        elif msg["timestamp"] > time.time() :
            raise Exception("timestamp must be less than now")
if __name__=="__main__":
    obj=listener(os.environ["MONGO_ADDRESS"],os.environ["KAFKA_ADDRESS"],os.environ["KAFKA_TOPIC"])
    obj.set_validate_function(validate)
    obj.listen()





