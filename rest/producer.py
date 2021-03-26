import logging
import sys
import time
from kafka import KafkaProducer
from connections_config import KAFKA_HOST,KAFKA_TOPIC

class KafkaHandler(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self)
        while True:
            try:
                #x=5/0
                self.producer = KafkaProducer(bootstrap_servers=[KAFKA_HOST])
                break
            except Exception as e:
                print("kafka bağlantısı kurulamadı:",e)
                print("1 saniye sonra yeniden denenecek")
            time.sleep(1)
        
        self.topic = KAFKA_TOPIC

    def emit(self, record):
        if 'kafka.' in record.name:
            return
        #time.sleep(10)
        msg = self.format(record)
        try:
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
            