import pymongo
import os
class mong:
    def __init__(self):
        #myclient = pymongo.MongoClient("mongodb://"+os.environ["MONGO_ADDRESS"])
        myclient = pymongo.MongoClient("mongodb://localhost:27017")
        mydb = myclient["locations"]
        self.cities_col = mydb["cities"]
        self.boroughs_col = mydb["boroughs"]

    def setCity(self,city_obj):
        self.cities_col.insert_one(city_obj)
    def setBorough(self,borough_obj,city_name=None):
        if city_name!=None:
            _city=self.cities_col.find_one({"name":city_name})
            borough_obj["cityId"]=_city["_id"]
        self.boroughs_col.insert_one(borough_obj)
    def getCity(self,args,city_name=None):
        que={}
        if city_name!=None:
            que["name"]=city_name
        for i in args.keys():
            que[i]=args[i]
        result=self.cities_col.find(que,{'_id': False})
        result=list(result)
        return result
    def getBorough(self,args,city_name=None,name=None):
        que={}
        if city_name!=None:
            city=self.cities_col.find_one({"name":city_name})
            que["cityId"]=city["_id"]
        if name!=None:
            que["name"]=name
        for i in args.keys():
            que[i]=args[i]
        result=self.boroughs_col.find(que,{'_id': False,"cityId":False})
        result=list(result)
        return result
    def updateCity(self,args,content,city_name=None):
        que={}
        if city_name!=None:
            que["name"]=city_name
        for i in args.keys():
            que[i]=args[i]
        new_values={"$set":content}
        self.cities_col.update(que,new_values)
    def deleteCity(self,content,city_name=None):
        if city_name!=None:
            content["name"]=city_name
        self.cities_col.delete_many(content)
    def updateBorough(self,args,content,city_name=None,name=None):
        que={}
        if city_name!=None:
            city=self.cities_col.find_one({"name":city_name})
            que["cityId"]=city["_id"]
        if name!=None:
            que["name"]=name
        new_values={"$set":content}
        self.boroughs_col.update_many(que,new_values)
    def deleteBorough(self,content,city_name=None,name=None):
        if city_name!=None:
            city=self.cities_col.find_one({"name":city_name})
            content["cityId"]=city["_id"]
        if name!=None:
            content["name"]=name
        self.boroughs_col.delete_many(content)