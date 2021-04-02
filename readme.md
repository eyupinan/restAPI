# Kartaca restAPI görevi
Görev unsurlarının tamamı yerine getirilmiştir.
GET,POST,PUT ve DELETE metodları için bir restAPI de endpoint'ler sunulmuştur.
restAPI gelen her bir request için bir thread içerisinden Kafka'ya log mesajı gönderir.
Bir consumer gelen bu log mesajlarını yakalayıp mongoDB içerisinde kaydeder.
Bir dashboard server'i mongoDB içerisindeki kayıtlara göre son bir saat için bir gecikme grafiği sergiler.
## Kullanımı
Bilgisayarınızdaki docker uygulaması üzerinde bu uygulamanın çalıştırılabilmesi için github üzerinden bir
dizine repository kopyalanır ve dizine gidilir.
```bat
git clone https://github.com/eyupinan/restAPI.git
cd restAPI
```
Bu dizin içerisinde 
```bat
docker-compose up --build
```
komutu çalıştırılır. Bu komut gerekli bağlılıkların kurulumunu docker içerisine yaptıktan sonra çalışmaya 
başlayacaktır.Uygulamanın config özellikleri .env dosyası üzerinden değiştirilebilir.
Aşağıda gösterilen yöntemlerle ```localhost:5000``` adresine request gönderilebilir.
RestAPI için gelen requestlerin gecikme durumlarının grafiği için
```localhost:8052``` adresine gidilir.

### GET method

Get metodu için url parametreleri ve query parametreleri sorgu işlemi için kullanılabilir.
Örnek jquery get method kullanımları:
```javascript
//bütün şehirlerin bilgilerini sorgular
$.get("http://localhost:5000/city",(data,status)=>{
    console.log(data)
    })
//url parametresi olarak verilen şehirin bilgilerini sorgular
$.get("http://localhost:5000/city/istanbul",(data,status)=>{
    console.log(data)
    })
//query parametresi olarak verilen şehrin bilgilerini sorgular
$.get("http://localhost:5000/city?name=istanbul",(data,status)=>{
    console.log(data)
    })
//istanbul şehrinde fatih ilçesinin bilgilerini sorgular
$.get("http://localhost:5000/istanbul/borough?name=fatih",(data,status)=>{
    console.log(data)
    })
//herhangi bir şehirdeki fatih ilçesini sorgular
$.get("http://localhost:5000/borough/fatih",(data,status)=>{
    console.log(data)
    })
```
### POST method
 POST metodu için url parametreleri,sorgu parametreleri ve request body'si yeni bir veri oluşturmak için kullanılır.
Örnek jquery POST kullanımları:
``` javascript
//bu request şehir oluşturur. body içerisinde verilen veriler şehir için özellik olarak kaydedilir.
$.post("http://localhost:5000/istanbul",json.stringify({"plaka":"34"}),(data,status)=>{
    console.log(data)
})
//bu requst istanbul şehri referans alınarak fatih ilçesi oluşturur. query parametresi olarak verilen veriler
//ilçe bilgileri olarak kaydedilir.
$.post("http://localhost:5000/istanbul/fatih?"+$.param({"population":"1234"}),(data,status)=>{
    console.log(data)
})
// borough dizini üzerine oluşturulan ilçeler şehir referans olarak göstermeyebilir.
$.post("http://localhost:5000/borough/fatih?"+$.param({"population":"1234"}),(data,status)=>{
    console.log(data)
})
```

### PUT method
PUT metodu için url parameteleri sorgu için query parametreleri ve body güncellenecek bilgiler için kullanılır.
Örnek jquery PUT kullanımları:
``` javascript
//istanbul şehrinin nüfusu özelliğini güncellemek için request body kullanılabilir
//aynı şekilde /istanbul/fatih veya /borough/fatih url yolları ile fatih ilçesi bilgileri güncellenebilir.
$.ajax({
    url: 'http://localhost:5000/istanbul',
    type: 'PUT',
	data:JSON.stringify({"population":15000000}),
    success: function(result) {
        console.log(result)
        }
});
// şehir veya ilçe için /update/<entity_name>/<value> şeklinde verilecek parametreler şehir için <entity_name>
//özelliğini <value> olarak verilen değer ile günceller.burada şehir veya ilçe ismi sorgu için 
// update dizini sonrası url parametreleri veya query parametreleri update datası olarak kullanılır

//bu request istanbul şehrinin nüfusunu günceller
$.ajax({
    url: 'http://localhost:5000/istanbul/update/population/15000000',
    type: 'PUT',
    success: function(result) {
        console.log(result)
        }
});
//bu request'de  yukarıdaki request ile aynı işi yapar ancak parametre olarak query parametreleri kullanılır
$.ajax({
    url: 'http://localhost:5000/istanbul/update?'+$.param({"population":15000000}),
    type: 'PUT',
    success: function(result) {
        console.log(result)
        }
});
``` 
Body bulundurmayan put metodu için geliştirilmiş update dizini standart put metodundan farklıdır.
body ile gönderilen put metodunda url parametreleri ve query parametreleri sorgu için kullanılır.
update dizinine gönderilen request'ler body gerektirmez ve normalden farklı olarak query parametrelerini yeni data olarak kullanır.

### DELETE method

delete metodu url parametreleri ve body içerisini sorgu için kullanır. Sorgu ile eşleşen veri databaseden silinir.
Örnek DELETE query sorguları:
``` javascript
//istanbul şehrini siler
$.ajax({
    url: 'http://localhost:5000/city',
    type: 'DELETE',
	data:JSON.stringify({"name":"istanbul"}),
    success: function(result) {
        console.log(result)
    }
});
//istanbul şehrinin fatih ilçesini siler
$.ajax({
    url: 'http://localhost:5000/istanbul/fatih',
    type: 'DELETE',
    success: function(result) {
        console.log(result)
    }
});
```
