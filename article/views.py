from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from django.contrib import messages
from .models import Article, Comment
from .forms import ArticleForm
from django.contrib.auth.decorators import login_required

def articles(request):
    if request.GET.get("keyword"):
        keyword = request.GET.get("keyword")
        articles = Article.objects.filter(title__contains = keyword)
    else:
        articles = Article.objects.all()
    context = {
        "articles" : articles
    }
    return render(request,"articles.html", context)

def index(request):
    #return HttpResponse('<h3>Anasayfa</h3>')
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles" : articles
    }
    return render(request,"dashboard.html", context)

@login_required(login_url="user:login")
def addarticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
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

def detail(request, id):
    article = get_object_or_404(Article, id = id)
    #comments = Comment.objects.filter(article = article)
    comments = article.comments.all()
    context = {
        "article" : article,
        "comments" : comments,
    }
    return render(request,"articleDetail.html", context)

@login_required(login_url="user:login")
def updateArticle(request, id):
    article = get_object_or_404(Article, id = id, author = request.user)
    form = ArticleForm(request.POST or None, request.FILES or None, instance = article)
    if form.is_valid():
        article = form.save(commit = False)
        article.author = request.user
        article.save()
        messages.warning(request, "Makale Başarıyla Güncellendi!")
        return redirect("article:dashboard")
    context = {
        "form" : form
    }
    return render(request,"updateArticle.html",context)

@login_required(login_url="user:login")
def deleteArticle(request, id):
    article = get_object_or_404(Article, author = request.user, id = id).delete()    
    messages.success(request,"Silme İşlemi Başarıyla Tamamlandı!")
    return redirect("article:dashboard")

def comment(request, id):
    article = get_object_or_404(Article, id = id)
    if request.method == "POST":
        author = request.user
        content = request.POST.get("content")
        if author and content:
            Comment.objects.create(author = author, contents = content, article = article)
        else:
            if not author:
                messages.error(request,"Lütfen Giriş Yapınız!")
            elif not content:
                messages.error(request,"Yorum Alanı Boş Bırakılamaz!")
    #return redirect("/articles/detail/" + str(id))
    return redirect(reverse("article:detail",kwargs = {"id" : id}))
