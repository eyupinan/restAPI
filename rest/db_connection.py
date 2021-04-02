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
    new_content=content.copy()
    if ref_name in ref:
        if ref[ref_name]!=None:
            item=collection.find_one(ref)
            if item==None:
                return 404
            new_content[content_ref_name]=item["_id"]
    return new_content
class mong:
    def __init__(self,mongo):
        self.db=mongo.db
    def setCity(self,content):
        if "name" in content:
            found=self.db.cities.find({"name":content["name"]})
            if len(list(found))!=0:
                return 409
        self.db.cities.insert_one(content)
        return 201
    
    def getCity(self,que):
        result=self.db.cities.find(que,{'_id': False})
        result=list(result)
        return result
    
    def updateCity(self,que,content):
        print(que,content)
        found=list(self.db.cities.find(que))
        print(found)
        if len(found)!=0:
            if len(content)!=0:
                new_values={"$set":content}
                
                self.db.cities.update_many(que,new_values)
                if "name" in content:
                    #eğer şehirde isim değişikliği yapılırsa bağlantılı olan ilçelerdeki şehir ismi de değiştirilir
                    self.db.boroughs.update_many({"city_name":que["name"]},
                     {"$set":{"city_name":content["name"]}})
                return 200
            else:
                return 204
        else:#eğer update edilmesi hedeflenen data bulunmuyor ise content ve url parametreleri ile bu data oluşturulur.
            new_content=merge_dict(que,content)
            self.setCity(new_content)
            return 201
    def deleteCity(self,content):
        # şehir silme yapılırken bu şehirleri referans gösteren ilçelerinde referans değerleri siliniyor
        found=list(self.db.cities.find(content))
        for _city in found:
            _id=_city["_id"]
            print(list(self.db.boroughs.find({"cityId":_id})))
            try:
                self.db.boroughs.update_many({"cityId":_id},{"$unset":{"cityId":_id}})
            except Exception as e:
                print(e)
        delete_result=self.db.cities.delete_many(content)
        if delete_result.deleted_count>0:
            return 200
        else:
            return 404
    def setBorough(self,content,ref):
        if len(ref)!=0:
            if ref["name"]!=None:
                # eğer şehir bulunmuyor ise verilen isimde bir şehir oluşturuluyor
                city_list=self.getCity(ref)
                if len(city_list)==0:
                    self.setCity(ref)
                #şehrin id'si ilçeye referans olarak atanıyor
                content=add_ref(self.db.cities,content,ref,"name","cityId")

        #eğer aynı isim ve referansa sahip ilçe varsa anlaşmazlık cevabı döndürülüyor
        if "name" in content:
            check={"name":content["name"]}
            found=list(self.db.boroughs.find(check))
            if len(found)!=0:
                return 409
        self.db.boroughs.insert_one(content)
        return 201
    def getBorough(self,que,ref):
        que=add_ref(self.db.cities,que,ref,"name","cityId")  
        result=self.db.boroughs.find(que,{'_id': False,"cityId":False})
        result=list(result)
        return result
    def updateBorough(self,que,content,ref):
        #eğer update edilecek veya oluşturulacak olan ilçenin şehri bulunmuyor ise oluşturulur
        if "name" in ref and ref["name"]!=None:
            found=self.getCity(ref)
            if len(found)==0:
                self.setCity(ref)
        #şehir referansı ekleniyor 
        # bu ilçenin var olup olmadığı kontrol ediliyor
        #eğer bu ilçe yok ise yeni bir ilçe olarak oluşturuluyor
        found=list(self.db.boroughs.find(que))
        if len(found)!=0:
            #body boş ise ve her hangi bir şehre referans da eklenmiyor ise boş body cevabı dönülüyor
            if len(content)!=0 or ("name" in ref and ref["name"]!=None):
                referenced_content=add_ref(self.db.cities,content,ref,"name","cityId") 
                new_values={"$set":referenced_content}
                self.db.boroughs.update_many(que,new_values)
                return 200
            else:
                return 204
        else:
            new_content=merge_dict(que,content)
            state=self.setBorough(new_content,ref)
            return state
    def deleteBorough(self,content,ref):
        content=add_ref(self.db.cities,content,ref,"name","cityId")
        delete_result=self.db.boroughs.delete_many(content)
        if delete_result.deleted_count>0:
            return 200
        else:
            return 404
        