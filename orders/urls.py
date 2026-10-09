from django.urls import path
from . import views

app_name = "orders"  # application namespace

urlpatterns = [
    path("", views.order_list, name="list"),
    path("create/", views.order_create, name="create"),
    path("<int:pk>/", views.order_detail, name="detail"),
    path("<int:pk>/download/<int:item_id>/", views.order_download, name="download"),
]