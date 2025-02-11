from django.shortcuts import render
from django.views import View
from products.models import Product,Category


class HomePageView(View):

    def get(self, request,category_slug=None):
        products = Product.objects.filter(is_available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = Product.objects.filter(category=category)
        return render(request, 'home/home.html',{'products':products,'categories':categories})
