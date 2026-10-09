from django.urls import path
from . import views

app_name = "cart"  # application namespace

urlpatterns = [
    path("", views.cart_detail, name="detail"),
    path("add/<int:service_id>/", views.cart_add, name="add"),
    path("remove/<int:service_id>/", views.cart_remove, name="remove"),
    path("clear/", views.cart_clear, name="clear"),
]