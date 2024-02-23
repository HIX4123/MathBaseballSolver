from django.urls import URLPattern, path
from myapp import views

urlpatterns = [path("", views.index)]
