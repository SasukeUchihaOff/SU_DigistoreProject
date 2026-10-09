from django.urls import path
from . import views

app_name = "catalog"            # пространство имён приложения

urlpatterns = [
    path("", views.service_list, name="service_list"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("<slug:slug>/", views.service_detail, name="service_detail"),
]