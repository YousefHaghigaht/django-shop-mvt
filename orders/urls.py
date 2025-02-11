from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('detail/<int:order_id>/',views.OrderDetailView.as_view(),name='detail_order'),
    path('create_order/',views.OrderCreateView.as_view(),name='create_order'),
    path('cart/',views.CartView.as_view(),name='cart'),
    path('add_cart/<int:product_id>/',views.CartAddView.as_view(),name='add_cart'),
    path('remove_cart/<int:product_id>/',views.CartRemoveView.as_view(),name='remove_product'),
    path('order_pay/<int:order_id>/', views.OrderPayView.as_view(), name='order_pay'),
    path('verify/', views.OrderVerify.as_view(), name='verify'),
]