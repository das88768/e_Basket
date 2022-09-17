from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

# Create your views here.
def index(request):
    products = Product.objects.all()
    # print(products)
    context = {
        'product' : products,
    }
    return render(request, 'index.html', context)

def about_us(request):
    category = Product.objects.all()
    context = {
        'categories' : category,
    }
    return render(request, "about.html", context)

def contact_us(request):
    return HttpResponse("This is contact page.")
                                                                                # render(request, 'index.html')
def search_product(request):
    return HttpResponse("This is search page.")

def track_order(request):
    return HttpResponse("This is track page.")

def checkout(request):
    return HttpResponse("This is checkout page.")

def product_view(request, id):
    category = Product.objects.all()
    # print(products)
    # Fetch a specific product with id and stores in product var.
    product = Product.objects.filter(id=id).values()
    # print(product)
    context = {
        'product' : product[0],
        'categories' : category,
    }
    
    return render(request, "product_detail.html", context)
    # {'product':product[0]}