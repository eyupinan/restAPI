from kafka import KafkaConsumer
from kafka import KafkaProducer
import pymongo
print("consumer geldi")
consumer = KafkaConsumer("KafkaDemo",bootstrap_servers='kafka:9093',value_deserializer=lambda x: x.decode("utf-8"))
#consumer = KafkaConsumer("KafkaDemo",bootstrap_servers='localhost:9092',value_deserializer=lambda x: x.decode("utf-8"))
myclient = pymongo.MongoClient("mongodb://mongodb:27017/")
print("connection:",myclient)
mydb = myclient["mydatabase4"]
mycol = mydb["mylogs"]

#mydict = { "name": "John", "address": "Highway 37" }

#x = mycol.insert_one(mydict)
#consumer=["GET,1111,12342134","GET,2222,4325352234"]
for msg in consumer:
    pieces=msg.value.split(",")
    #pieces=msg.split(",")
    new_log={"method":pieces[0],"delay":pieces[1],"timestamp":int(pieces[2])}
    x = mycol.insert_one(new_log)




