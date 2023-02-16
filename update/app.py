@app.route("/update/<string:id>",methods = ["GET","POST"])
def update(id):
    #GET KISMI = Get request neden kullanıyoruz = Verileri çekmek için kullanıyoruz verileri çektikten sonra , post request kullanıp o verileri düzenliyoruz.
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        #select * From nedir = Makale kısmına git ve id veya kullanıcı adını seç.
        sa = "Select * From makale where id = %s and author = %s"
        ok = cursor.execute(sa,(id,session["username"]))
        if ok == 0:
            flash("Böyle bir ürün yok veya bu işleme yetkiniz yok .","danger")
            return redirect(url_for("kontrol"))
        else:
            #fetchone = Sadece tek bir veri alsın anlamında
            #fetchall = Bütün verileri al değişkenidir bu nedir , ve bunu neden kullanmadık çünkü fetchall kullansaydık bütün verileri alırdı ama bizim istedğimiz 2 şey var id ve author yani kullanıcı adı o yüzden fetchone kullanıyoruz.
            makaleler = cursor.fetchone()
            form = MAKALEE()
            form.title.data = makaleler["title"]
            form.content.data = makaleler["content"]
            return render_template("update.html",form = form)

    else:
        #POST KISMI
        # buradaki title , content kısmı , mysql databasesinde kayıtlı olan yerlerin adı, ve bunları class sınıfı oluşturup bunları kullanıyoruz.
        form = MAKALEE(request.form)
        newTitle = form.title.data
        newContent = form.content.data
        newFiyat = form.fiyat.data
        #Select * From kullandık daha sonra bu id ve kullanıcı adı kısmında Update işlemleri yapıyoruz . 
        c = "Update makale Set title = %s,content = %s,fiyat = %s where id = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(c,(newTitle,newContent,newFiyat,id))
        # commit işlemi yapmazsanız bu işlem başarısız olur = Commit işlemi nedir yaptığınız işlemi kalıcı olarak veri tabanına kayıt eder.
        mysql.connection.commit()
        # bu flash komutu ise = Flash mesajı yaratmak için nedir yani bu = Mesela kullanıcı kayıt olduğunda o kısma flash mesajı yazarsak kullanıcı o flash mesajını görür
        #bunu nasıl kullanabiliriz. = from flask import Flask,flash olarak import etmeniz gerekmekedir. Daha sonra app.secret_key = "2312s" secret_key oluşturmazanız flash 
        #mesajınız kullanılmaz.
        
        flash("Ürün başarıyla güncellendi","success")
        return redirect(url_for("kontrol"))
        pass
