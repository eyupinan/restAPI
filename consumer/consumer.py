from kafka import KafkaConsumer
import pymongo
import logging
import time
log = logging.getLogger('kafka.conn')
log.setLevel(logging.CRITICAL)
while True:
    try:
        consumer = KafkaConsumer("restTopic",bootstrap_servers='kafka:9093',value_deserializer=lambda x: x.decode("utf-8"))
        myclient = pymongo.MongoClient("mongodb://mongodb:27017/")
        mydb = myclient["mydatabase4"]
        mycol = mydb["mylogs"]
        break
    except Exception as e:
        logging.warning("bağlantı kurulamadı:"+str(e))
        time.sleep(1)




for msg in consumer:
    pieces=msg.value.split(",")
    new_log={"method":pieces[0],"delay":pieces[1],"timestamp":int(pieces[2])}
    x = mycol.insert_one(new_log)




