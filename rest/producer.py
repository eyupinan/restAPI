"""from kafka import KafkaProducer
import kafka
import time
print("kafka:",kafka.__version__)
print("stfu")
class producer:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=['kafka:9093'])
    def send(self,msg):
        self.producer.send("KafkaDemo",bytes(msg,"utf-8"))
        
    
    
if __name__=="__main__":
    print("producer main geldi")
    obj=producer()
    while(True):
        time.sleep(2)
        obj.send("direk producer tarafindan")"""
import logging
import sys
import time
from kafka import KafkaProducer
from connections_config import KAFKA_HOST,KAFKA_TOPIC


class KafkaHandler(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self)
        self.producer = KafkaProducer(bootstrap_servers=[KAFKA_HOST])
        self.topic = KAFKA_TOPIC
        print("producer:",self.producer)

    def emit(self, record):
        if 'kafka.' in record.name:
            return
        #time.sleep(10)
        msg = self.format(record)
        print("record:",msg)
        try:
            # apply the logger formatter
            #msg = self.format(record)
            self.producer.send(self.topic, bytes(msg,"utf-8"))
            self.flush(timeout=1.0)
        except Exception as e:
            print(e)
            logging.Handler.handleError(self, record)

    def flush(self, timeout=None):
        self.producer.flush(timeout=timeout)

    def close(self):
        self.acquire()
        try:
            if self.producer:
                self.producer.close()

            logging.Handler.close(self)
        finally:
            self.release()
            