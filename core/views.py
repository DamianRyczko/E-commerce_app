from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem, Customer, Category, Address, OrderItem, Order
from .filters import ProductFilter  # Importujemy nasz filtr
from .forms import CategoryForm, ProductForm, AddressForm, CardForm, BlikForm
from django.contrib import messages
from django.urls import reverse

from .factory import customer_facade, employee_facade

@login_required(login_url='login')
def checkout(request):
    details = customer_facade.get_cart_details(request.user)
    cart_items = details['items']
    addresses = customer_facade.get_customer_address(request.user)
    selected_address = None
    customer = customer_facade.get_customer(request.user)

    if request.method == 'POST':

        if 'clear_address' in request.POST:
            if 'selected_shipping_address' in request.session:
                del request.session['selected_shipping_address']
            return redirect('checkout')

        addr_id = request.POST.get('address_id')
        if addr_id:
            request.session['selected_shipping_address'] = addr_id
            return redirect('checkout')

        if 'card_payment' in request.POST:
            if 'selected_shipping_address' in request.session:
                card_form = CardForm(request.POST)
                if card_form.is_valid():
                    customer_facade.checkout(request.user, request.session['selected_shipping_address'])
                    return redirect("orders")
                else:
                    messages.error(request, "Invalid card")
            else:
                messages.error(request, "Select Address")

        if 'blik_payment' in request.POST:
            if 'selected_shipping_address' in request.session:
                blik_form = BlikForm(request.POST)
                if blik_form.is_valid():
                    customer_facade.checkout(request.user, request.session['selected_shipping_address'])
                    return redirect("orders")
                else:
                    messages.error(request, "Invalid blik code")
            else:
                messages.error(request, "Select Address")



    session_addr_id = request.session.get('selected_shipping_address')

    if session_addr_id:
        selected_address = customer_facade.get_address(session_addr_id)



    card_form = CardForm()
    blik_form = BlikForm()

    context = {
        'customer': customer,
        'cart_items': cart_items,
        'addresses': addresses,
        'selected_address': selected_address,
        'card_form': card_form,
        'blik_form': blik_form,
    }
    return render(request, 'core/checkout.html', context)

#---------------------------- HOME ---------------------------
def home(request):
    products_queryset = customer_facade.get_products_for_display()
    # Nakładamy filtr.
    # request.GET zawiera parametry z URL (np. ?ordering=price)
    product_filter = ProductFilter(request.GET, queryset=products_queryset)


    data = customer_facade.get_cart_details(request.user)

    # Ważne: do szablonu przekazujemy przefiltrowaną listę (product_filter.qs)
    context = {
        'filter': product_filter,  # Przekazujemy obiekt filtra (by wyświetlić formularz)
        'products': product_filter.qs,  # Przekazujemy posortowane/przefiltrowane produkty
        'cart_items_count': data['count'],
    }

    return render(request, 'core/index.html', context)

#---------------------------- CUSTOMER ---------------------------
@login_required(login_url='login')
def orders(request):
    order_list = customer_facade.get_user_orders(request.user)
    return render(request, 'core/orders.html', {'order_list': order_list})

@login_required(login_url='login')
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            customer_facade.save_address(request.user, address)
            form.save_m2m()
            return redirect('checkout')
    else:
        form = AddressForm()
    return render(request, 'core/address.html', {'form': form})


@login_required(login_url='login')
def delete_address(request, address_id):
    if request.method == 'POST':

        address = customer_facade.get_address(address_id)

        if address:
            customer_facade.delete_address(address)
    return redirect('checkout')
#---------------------------- CART ---------------------------
@login_required(login_url='login')
def cart(request):
    data = customer_facade.get_cart_details(request.user)

    context = {
        'cart_items': data['items'],
        'cart_value': data['total_value'],
    }
    return render(request, 'core/cart.html', context)

@login_required(login_url='login')
def add_to_cart(request, product_id):
    if request.method == 'POST':
        try:
            qty = int(request.POST.get('quantity'))
            customer_facade.add_product(request.user, product_id, qty)
        except (ValueError, TypeError):
            pass


    #stops going back to top of the page a fter adding itmes to cart
    base_url = reverse('home')
    redirect_url = f"{base_url}#produkt-{product_id}"
    return redirect(redirect_url)



@login_required(login_url='login')
def update_quantity(request, product_id):
    if request.method == 'POST':
        try:
            customer_facade.update_quantity(request.user, product_id, int(request.POST.get('quantity')))
        except (ValueError, TypeError):
            # Handle case where quantity isn't a number
            pass

    return redirect('cart')

@login_required(login_url='login')
def delete_from_cart(request, product_id):
    if request.method == 'POST':
        customer_facade.remove_product(request.user, product_id)

    return redirect('cart')

#---------------------------- EMPLOYEE ---------------------------
def employee_products(request):
    products = employee_facade.get_all_products()
    return render(request, 'core/employee_products.html', {'products': products})


def employee_orders(request):
    orders = employee_facade.get_all_orders()
    return render(request, 'core/employee_orders.html', {'orders': orders})

def orders_sent(request, pk):
    employee_facade.send_order(pk)
    return redirect('employee_orders')


def orders_completed(request, pk):
    employee_facade.complete_order(pk)
    return redirect('employee_orders')


def employee_categories(request):
    categories = employee_facade.get_categories()
    return render(request, 'core/employee_categories.html', {'categories': categories})
def manage_category(request, pk=None):
    category = employee_facade.get_category(pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_obj = form.save(commit=False)

            employee_facade.save_category(category_obj)

            # Zapisujemy relacje Many-to-Many
            form.save_m2m()

            return redirect('employee_categories')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'core/category_add.html', {'form': form})

def delete_category(request, pk):
    if request.method == 'POST':
        employee_facade.delete_category(pk)
    return redirect('employee_categories')

def manage_product(request, pk = None):
    product = employee_facade.get_product(pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            product_obj = form.save(commit=False)
            employee_facade.save_product(product_obj)
            form.save_m2m()
            return redirect('employee_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'core/products_add.html', {'form': form})

def delete_product(request, pk):
    if request.method == 'POST':
        employee_facade.delete_product(pk)
    return redirect('employee_products')

