from django.urls import path
from . import views

app_name = 'shop'  # only if you want to namespace
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:id>/', views.product_detail, name='product_detail'),
]
