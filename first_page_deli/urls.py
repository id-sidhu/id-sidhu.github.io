from django.urls import path
from . import views
from .admin import coop_deli_admin_site


urlpatterns = [
    path("", views.index, name='index'),
    path("shelf/<str:shelf_name>", views.shelf_detail_view, name='shelf_detail_view'),
    path("<str:shelf_name>", views.on_sale_view, name='on_sale_view'),
    path('order/<int:product_id>/', views.place_order, name='place_order'),
    path('payment/placeholder/<int:order_id>/', views.payment_placeholder, name='payment_placeholder'),  # Corrected here
    path('shelf/BYOPizza/', views.build_your_own_pizza, name='build_your_own_pizza'),
    path('search/', views.search_view, name='search_view'),
]