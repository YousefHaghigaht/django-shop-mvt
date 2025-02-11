from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from .models import Product
from . import tasks
from django.contrib import messages
from utils import IsAdminMixin
from .forms import QuantityForm


class ProductDetailView(View):

    def get(self,request,product_id):
        product = get_object_or_404(Product,id=product_id)
        form = QuantityForm
        return render(request,'products/detail.html',{'product':product,'form':form})


class BucketObjectsView(IsAdminMixin,View):

    def get(self,request):
        objects = tasks.list_objects_task()
        return render(request,'products/bucket.html',{'objects':objects})


class DeleteObjectView(IsAdminMixin,View):

    def get(self,request,key):
        tasks.delete_object_task.delay(key)
        messages.success(request,'The object deleted .. ','success')
        return redirect('products:objects')


class DownloadObjView(IsAdminMixin,View):

    def get(self,request,key):
        tasks.download_object_task.delay(key)
        messages.success(request,'Start downloading...','success')
        return redirect('products:objects')
