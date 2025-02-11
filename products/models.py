from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField

class Category(models.Model):
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE,related_name='scategory',null=True,blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolut_url(self):
        return reverse('products:products_category',args=[self.slug])


class Product(models.Model):
    category = models.ManyToManyField(Category,related_name='products')
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    image = models.ImageField()
    is_available = models.BooleanField(default=True)
    price = models.IntegerField()
    description = RichTextField()

    def __str__(self):
        return self.name

