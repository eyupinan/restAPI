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
class boroughs_blueprint:
    def __init__(self,mong_obj):
        self.mong_obj=mong_obj
    def create_blueprint(self):
        borough_blue= Blueprint('boroughs', __name__)
        @borough_blue.route('/city/<city_name>/borough/<borough_name>',methods=["POST","GET","PUT","DELETE"])
        @borough_blue.route('/city/<city_name>/borough',methods=["POST","GET","PUT","DELETE"])
        @borough_blue.route('/borough/<borough_name>',methods=["POST","GET","PUT","DELETE"])
        @borough_blue.route('/borough',methods=["POST","GET","PUT","DELETE"])
        def borough(city_name=None,borough_name=None):
            ref={"name":city_name}# referans eklemek için parametre olarak verilir
            #ismi verilmiş olan şehrin id değeri yapılacak işleme dahil edilir
            if request.method=="POST":
                content=add_value(get_content(request),["name"],[borough_name])
                state=self.mong_obj.setBorough(content,ref)
                if state==201:
                    return Response("ilçe eklendi",status=201)
                else:
                    return Response("ilçe zaten bulunuyor",status=409)
            elif request.method=="GET":
                args_dict = request.args.to_dict()
                args_dict=add_value(args_dict,["name"],[borough_name])
                result=self.mong_obj.getBorough(args_dict,ref)
                if len(result)!= 0:
                    result_json={"boroughs":result}
                    js=jsonify(result_json)
                    return js
                else:
                    return Response("aranan ilçe bulunamadı",status=404)

            elif request.method=="PUT":
                content=get_content(request)
                if len(content)==0 and int(request.headers["Content-Length"])!=0:
                    return Response("body json tipi data içermelidir",status=400)
                args_dict=add_value(request.args.to_dict(),["name"],[borough_name])
                state=self.mong_obj.updateBorough(args_dict,content,ref)
                if state==200:
                    return Response("data güncellendi",status=state)
                elif state==201:
                    return Response("yeni data eklendi",status=state)
                elif state==204:
                    return Response("boş request body alındı",status=state)
            elif request.method=="DELETE":
                content=add_value(get_content(request),["name"],[borough_name])
                state=self.mong_obj.deleteBorough(content,ref)
                if state==200:
                    return Response("ilçe silindi",status=200)
                else:
                    return Response("ilçe bulunamadı",status=404)
        return borough_blue