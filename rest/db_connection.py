import pymongo
import os
def merge_dict(dict1,dict2):
    merged_dict={}
    if dict1!=None:
        merged_dict.update(dict1)
    if dict2!=None:
        merged_dict.update(dict2)
    return merged_dict  
def add_ref(collection,content,ref,ref_name,content_ref_name):
    if ref_name in ref:
        if ref[ref_name]!=None:
            item=collection.find_one(ref)
            content[content_ref_name]=item["_id"]
    return content
class mong:
    def __init__(self):
        #myclient = pymongo.MongoClient("mongodb://"+os.environ["MONGO_ADDRESS"])
        myclient = pymongo.MongoClient("mongodb://localhost:27017")
        mydb = myclient["locations"]
        self.cities_col = mydb["cities"]
        self.boroughs_col = mydb["boroughs"]

    def setCity(self,args=None,content=None):
        que=merge_dict(args,content)
        
        self.cities_col.insert_one(que)
        return True
    
    def getCity(self,que):
        result=self.cities_col.find(que,{'_id': False})
        result=list(result)
        return result
    
    def updateCity(self,que,content):
        new_values={"$set":content}
        self.cities_col.update(que,new_values)
        return True
    def deleteCity(self,content,city_name=None):
        self.cities_col.delete_many(content)
        return True
    def setBorough(self,args,content,ref):
        new_item=merge_dict(args,content)
        new_item=add_ref(self.cities_col,new_item,ref,"name","cityId")  
        self.boroughs_col.insert_one(new_item)
        return True
    def getBorough(self,que,ref):
        que=add_ref(self.cities_col,que,ref,"name","cityId")  
        result=self.boroughs_col.find(que,{'_id': False,"cityId":False})
        result=list(result)
        return result
    def updateBorough(self,que,content,ref):
        que=add_ref(self.cities_col,que,ref,"name","cityId")       
        new_values={"$set":content}
        self.boroughs_col.update_many(que,new_values)
        return True
    def deleteBorough(self,content,ref):
        content=add_ref(self.cities_col,content,ref,ref_name="name",content_ref_name="cityId")
        self.boroughs_col.delete_many(content)
        return True