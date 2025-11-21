from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from . import views
from .views import (
    home, category_list, category_create, category_delete,
    product_create, product_update, product_delete,
    ProductDetail, contact_view
)

urlpatterns = [
    path('', views.product_list, name='product_list'),  # Asosiy sahifa — product list

    path('home/', home, name='home'),

    path('categories/', category_list, name='category_list'),
    path('category/add/', category_create, name='category_create'),
    path('category/delete/<int:pk>/', category_delete, name='category_delete'),

    path('product/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('product/add/', product_create, name='product_create'),
    path('product/edit/<int:pk>/', product_update, name='product_update'),
    path('product/delete/<int:pk>/', product_delete, name='product_delete'),
    path('contact/', views.contact_view, name='contact'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
