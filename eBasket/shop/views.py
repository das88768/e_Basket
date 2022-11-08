from email import message
from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
import datetime
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
# create the view of 'home page' page
def index(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()[:16]
    category = Category.objects.all()
    context = {
        'product' : products,
        'cartItems' : cartItems,
        'category' : category
    }
    return render(request, 'index.html', context)

# create the view of 'about us' page
def about_us(request):
    category = Category.objects.all()
    context = {
        'category' : category,
    }
    return render(request, "about.html", context)

def contact_us(request):
    return HttpResponse("This is contact page.")
                                                                                # render(request, 'index.html')
def search_product(request):
    return HttpResponse("This is search page.")

def track_order(request):
    return HttpResponse("This is track page.")

# create the view of the cart page    
def cart(request):
    # if user is logged in, he will see the ordered products.
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    
    # if user is not logged in, he can't see the products and can't add the product in cart.
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, "cart.html", context)

# create the view of checkout page
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    # provides the ordered products data to the checkout page
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, "checkout.html", context)

# create the view of a specific product, page
def product_view(request, id):
    # only logged in user can add products.
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    # anonymous user can not add products to the cart.
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    category = Category.objects.all()
    # print(products)
    # Fetch a specific product with id and stores in product var.
    product = Product.objects.filter(id=id).values()
    # print(product)
    context = {
        'product' : product[0],
        'category' : category,
        'cartItems' : cartItems
    }
    
    return render(request, "product_detail.html", context)
    # {'product':product[0]}

# view which helps to change product quantity in the cart using js.
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    # print('Action:', action)
    # print('poroductId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = orderItem.quantity + 1
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity - 1
    elif action == 'delete':
        orderItem.quantity = 0

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)

# view which process the order and store shipping address in the database
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        # save and store the shipping address of the logged in user
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            country = data['shipping']['country'],
            zipcode = data['shipping']['zipcode']
        )

    else:
        print("Customer is not logged in!")

    return JsonResponse("Payment completed!", safe=False)

def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            password = form.cleaned_data.get("password1")
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            user = authenticate(request, username = username, password=password)
            Customer.objects.create(user=user, name=username, email=email)
            messages.success(request, f"Profile is created for {username}")
            return redirect('login')

    context = {'form' : form}
    return render(request, "register.html", context)

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.info(request, "Password or Username is Incorrect")

    context = {}
    return render(request, "login.html", context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def fasionPage(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    products = Product.objects.filter(category__name = "Fashion")
    category = Category.objects.all()
    cat = products[0].category
    context = {
        'product' : products,
        'cartItems' : cartItems,
        'category' : category,
        'cat' : cat
    }
    return render(request, 'category_page.html', context)

def electronicsPage(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    products = Product.objects.filter(category__name = "Electronics")
    category = Category.objects.all()
    cat = products[0].category
 
    context = {
        'product' : products,
        'cartItems' : cartItems,
        'category' : category,
        'cat' : cat
    }
    return render(request, 'category_page.html', context)

def mobilesPage(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    products = Product.objects.filter(category__name = "Mobiles")
    category = Category.objects.all()
    cat = products[0].category
 
    context = {
        'product' : products,
        'cartItems' : cartItems,
        'category' : category,
        'cat' : cat
    }
    return render(request, 'category_page.html', context)

def booksPage(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    products = Product.objects.filter(category__name = "Books")
    category = Category.objects.all()
    cat = products[0].category
 
    context = {
        'product' : products,
        'cartItems' : cartItems,
        'category' : category,
        'cat' : cat
    }
    return render(request, 'category_page.html', context)

def home_accessories_and_furniturePage(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    products = Product.objects.filter(category__name = "Home_Accessories_and_Furnitures")
    category = Category.objects.all()
    cat = products[0].category
 
    context = {
        'product' : products,
        'cartItems' : cartItems,
        'category' : category,
        'cat' : cat
    }
    return render(request, 'category_page.html', context)

def all_products(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    category = Category.objects.all()
    cat = "All Products"
 
    context = {
        'product' : products,
        'cartItems' : cartItems,
        'category' : category,
        'cat' : cat
    }
    return render(request, 'category_page.html', context)
