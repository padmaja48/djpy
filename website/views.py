from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import Products, AuthUser
from .forms import AuthUserCreationForm # Assuming you have a forms.py with AuthUserCreationForm

# ----------------- Core E-commerce Views -----------------

def welcome(request):
    """Creative welcome page"""
    return render(request, 'websites/welcome.html')

def home(request):
    """Product List Page (now at /home/)"""
    products = Products.objects.all()
    context = {'products': products}
    return render(request, 'websites/index.html', context)

def product_detail(request, pk):
    """Product Detail/View Page & 'Add to Cart' functionality"""
    product = get_object_or_404(Products, pk=pk)
    
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id = str(product.id)
        
        if product_id not in cart:
            cart[product_id] = 1
        else:
            cart[product_id] += 1
        
        request.session['cart'] = cart
        
        # print statement for debugging, safe to remove later
        print("Session Cart after update:", request.session.get('cart'))
        
        return redirect('cart')
    
    context = {'product': product}
    return render(request, 'websites/product_detail.html', context)

@login_required(login_url='login')
def cart(request):
    """Cart Page"""
    cart_items = request.session.get('cart', {})
    products_in_cart = []
    total_price = 0
    
    # Get all products in the cart from the database
    product_ids = [int(p_id) for p_id in cart_items.keys()]
    products = Products.objects.filter(id__in=product_ids)

    for product in products:
        quantity = cart_items[str(product.id)]
        subtotal = product.price * quantity
        total_price += subtotal
        
        products_in_cart.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
            
    context = {
        'products_in_cart': products_in_cart,
        'total_price': total_price
    }
    return render(request, 'websites/cart.html', context)

@login_required(login_url='login')
def update_cart(request):
    """Updates product quantity in the cart"""
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        
        cart = request.session.get('cart', {})
        
        if product_id and action:
            product_id = str(product_id)
            if action == 'add':
                cart[product_id] = cart.get(product_id, 0) + 1
            elif action == 'remove':
                cart[product_id] = cart.get(product_id, 0) - 1
                if cart[product_id] <= 0:
                    del cart[product_id]
            request.session['cart'] = cart
    
    return redirect('cart')

@login_required(login_url='login')
def checkout(request):
    """Renders the checkout/payment page."""
    cart_items = request.session.get('cart', {})
    products_in_cart = []
    total_price = 0
    
    product_ids = [int(p_id) for p_id in cart_items.keys()]
    products = Products.objects.filter(id__in=product_ids)

    for product in products:
        quantity = cart_items[str(product.id)]
        subtotal = product.price * quantity
        total_price += subtotal
        
        products_in_cart.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
            
    context = {
        'products_in_cart': products_in_cart,
        'total_price': total_price
    }
    return render(request, 'websites/payment.html', context)


@login_required(login_url='login')
def payment(request):
    """
    Handles the final order placement and clears the cart.
    This view is accessed after a successful 'payment'.
    """
    if request.method == 'POST':
        if 'cart' in request.session:
            # Here you would typically process the payment and save the order to the database.
            print("Order placed! Cart contents:", request.session['cart'])
            del request.session['cart']
        return render(request, 'websites/checkout_complete.html')

    return redirect('cart')

# ----------------- Authentication Views -----------------

def signup(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = AuthUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthUserCreationForm()
    return render(request, 'websites/signup.html', {'form': form})

def login(request):
    """Handles user login."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'websites/login.html', {'error': 'Invalid username or password'})
    return render(request, 'websites/login.html')

def logout(request):
    """Logs the user out."""
    auth_logout(request)
    return redirect('login')

# ----------------- Other Views -----------------

def search(request):
    """Handles product search functionality."""
    query = request.GET.get('q')
    if query:
        products = Products.objects.filter(name__icontains=query)
    else:
        products = Products.objects.all()
    context = {'products': products}
    return render(request, 'websites/index.html', context)