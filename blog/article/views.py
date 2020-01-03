from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from .models import Article
from .forms import ArticleForm
def index(request):
    #return HttpResponse('<h3>Anasayfa</h3>')
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles" : articles
    }
    return render(request,"dashboard.html", context)

def addarticle(request):
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        article = form.save(commit = False)
        article.author = request.user
        article.save()
        messages.warning(request, "Makale Başarıyla Kayıt Edildi!")
        return redirect("article:dashboard")
    context = {
        "form" : form
    }
    return render(request,"addarticle.html", context)

def updatearticle(request, id):
    pass

def deletearticle(request, id):
    article = get_object_or_404(Article, author = request.user, id = id).delete()    
    messages.success(request,"Silme İşlemi Başarıyla Tamamlandı!")
    return redirect("article:dashboard")