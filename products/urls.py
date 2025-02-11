from django.urls import path,include
from . import views
from home.views import HomePageView

app_name = 'products'

bucket_urls = [
    path('',views.BucketObjectsView.as_view(),name='objects'),
    path('delete_obj/<str:key>/',views.DeleteObjectView.as_view(),name='delete_obj'),
    path('dl_obj/<str:key>/',views.DownloadObjView.as_view(),name='dl_obj')
]

urlpatterns = [
    path('detail/<int:product_id>/',views.ProductDetailView.as_view(),name='detail'),
    path('bucket/',include(bucket_urls)),
    path('category/<slug:category_slug>/',HomePageView.as_view(),name='products_category')
]