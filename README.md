## Django FrameWork ile Geliştirilmiş Blog Projesi

### Kullanım:

- Python ile sanal bir çalışma ortamı oluşturun:

    Terminalde `python -m venv sanalOrtamAdı` komutunu yazarak oluşturabilirsiniz.

- Sanal ortam oluşturma işlemi bittikten sonra sanal çalışma ortamını aktifleştirin. Sanal ortamımızın adını **myvenv** olarak belirlemiş olduğumuzu varsayalım:

    > Windows kullanıcıları için:

    Terminalde iken sanal ortamı oluşturduğumuz dizin yoluna gelelim. Bunu `cd` (change directory) komutu ile yapabilirsiniz. Sanal ortamın bulunduğu dizinde iken `myvenv\Scripts\activate`
komutu ile sanal ortamımızı aktifleştirelim. Burada yaptığımız şey aslında sanal ortam klasörümüzün(myvenv) içindeki Scripts klasörünün içindeki activate dosyasını çalıştırma işlemidir.
Yani bu işlemi şu şekilde de yapabilirdik. `cd myvenv\Scripts` komutu ile Scripts klasörünün içine gidip `activate` yazabilirdik. Ya da sırasıyla `cd myvenv`, `cd Scripts`, `activate` ile 2 defa
dizin değiştirme komutu yazmış ve sonrasında ise bin dizininin içindeki activate dosyasını çalıştırmış olacaktık. Bu alternatif işlemlerin hepsi aynıdır. Konu ile ilgili olmasa da bu konuda
bazen kafa karışıklığı olabildiğini farkettiğim için bu bilgiyi paylaşmak istedim.

    > Linux kullanıcıları için:
    
    Terminalde iken sanal ortamı oluşturduğumuz dizin yoluna gelelim ve `source myvenv/bin/activate` komutu ile sanal ortamımızı aktifleştirelim.

- Sanal ortamımızı aktifleştirdikten sonra projede kullanılmış, yani projenin düzgün çalışabilmesi için gerekli uygulamaları yükleyelim:

    Öncelikle pip(python paket yükleyicisi) yükseltme işlemini yapalım:
    
    Terminalde iken `python -m pip install --upgrade pip` komutunu yazarak işlemin tamamlanmasını bekleyelim.

    pip yükseltme işlemi tamamlandıktan sonra terminalde dizin yolunu repo(Clone yapılan) klasörümüz olacak şekilde değiştirelim. Bulunduğumuz dizinde requirements.txt dosyasının bulunduğuna emin olalım.
Bunu kontrol etmek için Windows ortamında `dir` komutunu Linux ortamında ise `ls` komutunu kullanabilirsiniz.

    Proje dizinimize geldikten sonra `pip install -r requirements.txt` komutunu yazalım ve işlemin tamamlanmasını bekleyelim. Bu komut ile requirements.txt dosyasının içerisindeki uygulamalar
en üstteki satırdan başlayarak sırası ile sanal ortamımıza pip tarafından kurulacaktır.

    Yükleme işlemi tamamlandıktan sonra proje klasörümüze(Clone yapılan reponun içindeki blog adındaki klasör. Yani requirements.txt nin olduğu dizindeki blog klasörü) girelim. Bulunduğumuz dizinde
**manage.py** dosyasının olduğuna emin olalım ve terminalde `python manage.py runserver` komutunu yazarak sunucumuzu çalıştıralım.
    
    **Not**: Admin paneline `127.0.0.1:8000/admin` url adresine giderek `Kullanıcı Adı = anka` ve `Parola = FDSA1234` bilgileri ile giriş yaparak ulaşabilirsiniz. Yeni bir süper kullanıcı oluşturmak için ise yine manage.py dosyasının olduğu dizinde `python manage.py createsuperuser` komutunu kullanabilirsiniz. Komutu yazıp onayladıktan sonra sırası ile kullanıcı adı, e-mail(opsiyonel), parola ve tekrar parolanızı girerek süper yetkili bir kullanıcı oluşturarak bu kullanıcı ile de admin paneline ulaşabilirsiniz.
    
    |Blog Projesi|
    |:--:|
    |![Intro](https://github.com/zumrudu-anka/Blog-Project-With-Django/blob/master/presentationMedia/1.gif)|
    |![Intro](https://github.com/zumrudu-anka/Blog-Project-With-Django/blob/master/presentationMedia/2.gif)|
    |![Intro](https://github.com/zumrudu-anka/Blog-Project-With-Django/blob/master/presentationMedia/3.gif)|
    |![Intro](https://github.com/zumrudu-anka/Blog-Project-With-Django/blob/master/presentationMedia/4.gif)|
    
    
