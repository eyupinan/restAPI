import os
import base64
translated_string=""
for i in range(500):
    message=str(i)
    message_bytes=message.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    try:
        dosya=open("kartaca/"+base64_message,"r")
        veri=dosya.readlines()
        sp=veri[0].split(" ")
        for i in sp:
            dec=int(i,2)
            translated_string+=chr(dec)
    except Exception as e :
        print(e)
    
dosya=open("challenge.txt","w",encoding='utf8')
dosya.write(translated_string)
dosya.close()
