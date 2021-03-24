from kafka import KafkaConsumer
from kafka import KafkaProducer
import pymongo
print("consumer geldi")
consumer = KafkaConsumer("restTopic",bootstrap_servers='kafka:9093',value_deserializer=lambda x: x.decode("utf-8"))
myclient = pymongo.MongoClient("mongodb://mongodb:27017/")
print("connection:",myclient)
mydb = myclient["mydatabase4"]
mycol = mydb["mylogs"]

for msg in consumer:
    pieces=msg.value.split(",")
    new_log={"method":pieces[0],"delay":pieces[1],"timestamp":int(pieces[2])}
    x = mycol.insert_one(new_log)




