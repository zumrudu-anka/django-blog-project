"""
Basit, cache tabanlı istek sınırlayıcı.

Kaba kuvvet giriş denemelerini, toplu sahte kayıtları ve yorum/makale spamını
yavaşlatmak içindir. Gerçek bir DDoS'u uygulama katmanında durdurmak mümkün
değildir; o iş Cloudflare veya nginx `limit_req` gibi önde duran bir katmanın
görevidir.
"""
import logging
from functools import wraps

from django.core.cache import cache
from django.shortcuts import render

logger = logging.getLogger(__name__)


def client_ip(request):
    # Uygulama tek bir ters proxy (nginx vb.) arkasında çalışıyor. Proxy gerçek
    # istemci adresini X-Forwarded-For listesinin SONUNA ekler; istemcinin
    # kendisi başa sahte değerler yazabileceği için en sağdaki değeri alıyoruz.
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[-1].strip()
    return request.META.get("REMOTE_ADDR", "")


def _hit(cache_key, period):
    """Penceredeki sayacı bir artırır ve yeni değeri döndürür."""
    cache.add(cache_key, 0, period)
    try:
        return cache.incr(cache_key)
    except ValueError:
        cache.set(cache_key, 1, period)
        return 1


def ratelimit(key, limit, period, by = "ip"):
    """
    POST isteklerini `period` saniyelik pencerede en fazla `limit` kez kabul eder.
    `by="user"` giriş yapmış kullanıcıyı, `by="ip"` istemci IP'sini sayar.
    """
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.method != "POST":
                return view(request, *args, **kwargs)

            if by == "user" and request.user.is_authenticated:
                ident = "u{}".format(request.user.pk)
            else:
                ident = client_ip(request)
            cache_key = "rl:{}:{}".format(key, ident)

            try:
                count = _hit(cache_key, period)
            except Exception:
                # Sayaç tutulamıyorsa (ör. cache tablosu yok) siteyi çökertmek yerine
                # isteği geçir; sınırlama bu süre boyunca devre dışı kalır.
                logger.exception("Hız sınırlayıcı cache'e erişemedi; istek sınırlanmadan geçirildi.")
                return view(request, *args, **kwargs)

            if count > limit:
                context = {"wait_minutes": max(1, period // 60)}
                return render(request, "429.html", context, status = 429)
            return view(request, *args, **kwargs)
        return wrapper
    return decorator
