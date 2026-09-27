from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve
from article import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = "index"),
    path('about', views.about, name = "about"),
    path('articles/',include('article.urls')),
    path('user/',include('user.urls')),
    # Kullanıcıların yüklediği görseller (profil fotoğrafı, kapak). `static()` yardımcısı
    # yalnızca DEBUG açıkken çalıştığı için canlıda da Django sunuyor; küçük bir blog
    # için yeterli. Trafik artarsa bu işi nginx'e veya bir CDN'e devredin.
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
