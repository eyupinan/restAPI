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
Uygulamaya tamamen etkisiz rastgele request'ler gönderen bir ```client.html``` dosyası eklenmiştir. Bu uygulama basılan butonlara göre istek gönderir.

Log dosyasının görüntülenmesi için 
```docker cp restAPI_inan:/usr/src/app/rest /<kopyalanmak istenen adres>```
komutu kullanılabilir.
Mongodb bağlantısı mongonun expose edildiği porttan host cihazda görüntülenebilir.
## NOT!!! 
Bilgisayarınızda çalışmakta olan bir kafka serveri eğer docker içerisindeki kafka ile çakışacak olursa 
``` .env ``` dosyasından ```kafka_outside_port``` değeri değiştirilerek kafka outside servis portu değiştirilebilir.
Challenge de özellikle istenmemiş olmasıdan dolayı ve kullanım kolaylığı için jwt eklenmemiştir
## RestAPI Ayrıntılar
restAPI içerisinde tamamen etkisiz isteklerin gönderilebilmesi için sadece ```localhost:5000/``` adresi  kullanılır.
Bu adreslere gönderilen get,post,put ve delete istekleri tamamen etkisizdir ve sistem tarafından cevap olarak sadece istek tipi ve 0-3 saniye arasında rastgele bir delay değeri geri gönderilir.Örnek olarak 
```javascript
$.ajax({
    url: 'http://localhost:5000/',
    type: "GET",//POST,PUT veya DELETE komutlarıda kullanılabilir.
    success: function(result) {
        console.log(result)
        }
});
```
bu komut etkisizdir ve console ekranına ```get method <delay>``` yazar.

Rest api içerisinde şehir ve ilçeler için basit bir sistem geliştirilmiştir.Şehir görüntüleme,ekleme,güncelleme veya silme işlemleri için  ```/city/<şehir_ismi>``` adresine istek gönderilebilir. Aynı işlemler ilçeler için ```/borough/<ilçe_ismi>``` veya ```/city/<şehir_ismi>/borough/<ilçe_ismi>``` adresine istek gönderilerek gerçekleştirilebilir.
Aşağıda bu adreslerin kullanım örnekleri verilmiştir.

### GET method
Get metodunda url ve query parametreleri sorgu için kullanılmıştır.
```javascript
//bütün şehirlerin bilgilerini sorgular
$.get("http://localhost:5000/city",(data,status)=>{
    console.log(data)
    })
//url parametresi olarak verilen şehirin bilgilerini sorgular
$.get("http://localhost:5000/city/istanbul",(data,status)=>{
    console.log(data)
    })
//url parametresi olan istanbul şehrinde query parametresi olan fatih ismine sahip ilçeyi sorgular
$.get("http://localhost:5000/city/istanbul/borough",{"name":"fatih"},(data,status)=>{
    console.log(data)
    })
```
### POST method
POST metodunda url parametreleri ve request body'si eklenecek data olarak kullanılır.
``` javascript
//bu request sadece istanbul adına sahip olan bir şehir oluşturur
$.post("http://localhost:5000/city/istanbul",(data,status)=>{
    console.log(data)
})
//bu request istanbul şehri referansına sahip fatih adında içe oluşturur ve nüfus özelliği body içerisindeki değer olarak atanır
$.post("http://localhost:5000/city/istanbul/borough/fatih",JSON.stringify({"population":1234}),(data,status)=>{
    console.log(data)
})
```

### PUT method
PUT metodu için url parameteleri sorgu için query parametreleri ve body güncellenecek bilgiler için kullanılır.
Örnek jquery PUT kullanımları:
``` javascript
//bu request eğer istanbul adında bir şehir yok ise oluşturur ve nüfus değerini değiştirir.
//eğer istanbul adında bir şehir var ise bu şehirin nüfus değerini değiştirir.
$.ajax({
    url: 'http://localhost:5000/city/istanbul',
    type: 'PUT',
	data:JSON.stringify({"population":15000000}),
    success: function(result) {
        console.log(result)
        }
});
//query parametreleri de sorgu amacı ile kullanılabilir.
$.ajax({
    url: 'http://localhost:5000/city?'+$.param({"name":"istanbul"}),
    type: 'PUT',
    success: function(result) {
        console.log(result)
        }
});
//bu request de eğer bulunmuyor ise istanbul şehri ve fatih ilçesi oluştururlur. Fatih ilçesi zaten bulunuyor ise 
//ilçenin şehir referansı istanbul olarak atanır.
$.ajax({
    url: 'http://localhost:5000/city/istanbul/borough/fatih'
    type: 'PUT',
    success: function(result) {
        console.log(result)
        }
});
``` 


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
    url: 'http://localhost:5000/city/istanbul/borough/fatih',
    type: 'DELETE',
    success: function(result) {
        console.log(result)
    }
});
```

## Anahtar kod : 
``` gAAAAABgUI2G_hG13_Ix3R2OGUA8k4Njj3LOOy7-MPMt71MziNfr_aDCvnuqvxPpOYZYzlpHL_SGGtbut5W7ibF3129gkKeCOU9RodUbSW3NxvvRE0qI095R_LURsbwqBO7ngzJdSzl_XFhtA8lW6MdADW1CMa6y5_-DpVutUjm8agE8Os_CmTwVUlR3OCCanwTdIz4ZSGhhABEILPo6HV3faEGxk9wKPQ== ```
