import logging
import sys
import time
import os
from kafka import KafkaProducer
import json
#os.environ["KAFKA_ADDRESS"]="localhost:9092"
#os.environ["KAFKA_TOPIC"]="restTopic"
kafkaAdress=os.environ["KAFKA_ADDRESS"]
kafkaTopic=os.environ["KAFKA_TOPIC"]
class KafkaHandler(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self)
        while True:
            try:
                self.producer = KafkaProducer(bootstrap_servers=[kafkaAdress],value_serializer=lambda m: json.dumps(m).encode('utf-8'))
                break
            except Exception as e:
                print("kafka bağlantısı kurulamadı:",e)
                print("1 saniye sonra yeniden denenecek")
            time.sleep(1)
        
        self.topic = kafkaTopic

    def emit(self, record):
        if 'kafka.' in record.name:
            return
        msg = self.format(record)
        try:
            pieces=msg.split(",")
            new_message={"method":pieces[0],"delay":pieces[1],"timestamp":int(pieces[2])}
            self.producer.send(self.topic, new_message)
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
            