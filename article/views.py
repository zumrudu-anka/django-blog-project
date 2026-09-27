from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.views.decorators.http import require_POST
from blog.ratelimit import ratelimit
from .models import Article, Comment
from .forms import ArticleForm


def _article_list():
    return Article.objects.select_related("author").annotate(comment_count = Count("comments")).order_by("-created_date")


def index(request):
    context = {
        "latest" : _article_list()[:3],
        "article_count" : Article.objects.count(),
    }
    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html")


def articles(request):
    keyword = request.GET.get("keyword", "").strip()
    articles = _article_list()
    if keyword:
        articles = articles.filter(Q(title__icontains = keyword) | Q(content__icontains = keyword))
    page = Paginator(articles, 6).get_page(request.GET.get("page"))
    context = {
        "page" : page,
        "keyword" : keyword,
    }
    return render(request, "articles.html", context)


def detail(request, id):
    article = get_object_or_404(Article.objects.select_related("author"), id = id)
    context = {
        "article" : article,
        "comments" : article.comments.select_related("author"),
    }
    return render(request, "articleDetail.html", context)


@login_required(login_url="user:login")
def dashboard(request):
    articles = _article_list().filter(author = request.user)
    context = {
        "articles" : articles,
        "comment_total" : sum(a.comment_count for a in articles),
    }
    return render(request, "dashboard.html", context)


@login_required(login_url="user:login")
@ratelimit("article", limit = 10, period = 60 * 60, by = "user")
def addarticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        article = form.save(commit = False)
        article.author = request.user
        article.save()
        messages.success(request, "Makale başarıyla yayınlandı.")
        return redirect("article:dashboard")
    context = {
        "form" : form,
        "heading" : "Yeni makale",
        "submit_label" : "Yayınla",
    }
    return render(request, "articleForm.html", context)


@login_required(login_url="user:login")
def updateArticle(request, id):
    article = get_object_or_404(Article, id = id, author = request.user)
    form = ArticleForm(request.POST or None, request.FILES or None, instance = article)
    if form.is_valid():
        form.save()
        messages.success(request, "Makale başarıyla güncellendi.")
        return redirect("article:dashboard")
    context = {
        "form" : form,
        "heading" : "Makaleyi düzenle",
        "submit_label" : "Değişiklikleri kaydet",
        "article" : article,
    }
    return render(request, "articleForm.html", context)


@require_POST
@login_required(login_url="user:login")
def deleteArticle(request, id):
    get_object_or_404(Article, author = request.user, id = id).delete()
    messages.success(request, "Makale silindi.")
    return redirect("article:dashboard")


@require_POST
@login_required(login_url="user:login")
@ratelimit("comment", limit = 5, period = 60, by = "user")
def comment(request, id):
    article = get_object_or_404(Article, id = id)
    content = request.POST.get("content", "").strip()
    if article.author_id == request.user.id:
        messages.error(request, "Kendi makalenize yorum yapamazsınız.")
    elif content:
        Comment.objects.create(author = request.user, contents = content[:200], article = article)
        messages.success(request, "Yorumunuz eklendi.")
    else:
        messages.error(request, "Yorum alanı boş bırakılamaz.")
    return redirect(article.get_absolute_url() + "#yorumlar")
