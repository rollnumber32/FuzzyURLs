from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("short", views.short, name="short"),
    path("mail", views.mailing, name="mail"),
    path("<str:uid>", views.open_url, name="open_url"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
