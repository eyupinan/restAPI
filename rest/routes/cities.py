from flask import Blueprint, request,Response,jsonify
def get_content(req):
    try:
        content = req.get_json(force=True)
    except:
        content={}
    return content
def add_value(args,entity_name_list,value_list):
    for index in range(len(entity_name_list)):
        if value_list[index]!=None:
            args[entity_name_list[index]]=value_list[index]
    return args
class cities_blueprint:
    def __init__(self,mong_obj):
        self.mong_obj=mong_obj
    def create_blueprint(self):
        cities_blue= Blueprint('cities', __name__)
        @cities_blue.route('/city',methods=["POST","GET","PUT","DELETE"])
        @cities_blue.route('/city/<city_name>',methods=["POST","GET","PUT","DELETE"])
        def cities(city_name=None):
            if request.method=="POST":
                content=get_content(request)
                content=add_value(content,["name"],[city_name])
                state=self.mong_obj.setCity(content)
                if state==201:
                    return Response("yeni data oluşturuldu",status=201)
                else:
                    return Response("bu isme sahip şehir zaten var",status=409)
            elif request.method=="GET":
                args_dict=request.args.to_dict()
                args_dict=add_value(args_dict,["name"],[city_name])
                result_arr=self.mong_obj.getCity(args_dict)
                if len(result_arr):
                    response_json={"cities":result_arr}
                    js=jsonify(response_json)
                    return js
                else:
                    return Response("aranan şehir bulunamadı",status=404)
            elif request.method=="PUT":
                content=get_content(request)
                if len(content)==0 and int(request.headers["Content-Length"])!=0:
                    return Response("body json tipi data içermelidir",status=400)
                args_dict=add_value(request.args.to_dict(),["name"],[city_name])
                print(args_dict,content)
                state=self.mong_obj.updateCity(args_dict,content)
                if state==200:
                    return Response("data güncellendi",status=200)
                elif state==201:
                    return Response("yeni data oluşturuldu",status=201)
                elif state==204:#boş body kullanıldığında dönülen değer
                    return Response("boş request body alındı",status=200)

            elif request.method=="DELETE":
                content=add_value(get_content(request),["name"],[city_name])
                state=self.mong_obj.deleteCity(content)
                if state==200:
                    return Response("şehir silindi",status=200)
                else:
                    return Response("şehir bulunamadı",status=404)
        return cities_blue

 