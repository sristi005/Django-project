from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

from core.models import Category, Customer, Order, Login, Menu


def signin_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Please fill in all fields")
            return render(request, "signin.html")

        try:
            user = Login.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect('home_page')
            elif user.password == password:
                user.password = make_password(password)
                user.save(update_fields=['password'])
                request.session['user_id'] = user.id
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect('home_page')
            else:
                messages.error(request, "Invalid password")
        except Login.DoesNotExist:
            messages.error(request, "No account found with this email")

    return render(request, "signin.html")


def Signin(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        log_Obj = Login.objects.create(
            first_name=first_name, last_name=last_name,
            email=email, password=make_password(password)
        )
        request.session['user_id'] = log_Obj.id  # auto-login after signup
        messages.success(request, "Account created successfully!")
        return redirect('home_page')

    return render(request, "login.html")


def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out")
    return redirect('home_page')

def home(request):
    if request.method == "POST":
        cust_name = request.POST['name']
        cust_address = request.POST['cust_address']
        cust_phone = request.POST['cust_phone']
        cust_email = request.POST['cust_email']

        cust_Obj = Customer()
        cust_Obj.cust_name = cust_name
        cust_Obj.cust_email = cust_email
        cust_Obj.cust_phone = cust_phone
        cust_Obj.cust_address = cust_address
        cust_Obj.save()
        return redirect('success_page')

    return render(request, "home.html")


## for users use(home)


def menu(request):
    return render(request,"base1.html")
    # items = Menu.objects.all()
    # return render(request, "menu.html", {"items": items})

def coffee(request):
    items = Menu.objects.filter(item_category__name='Coffees')  ##coffee
    return render(request, "coffee.html", {"items": items})


def fri(request):
    items = Menu.objects.filter(item_category__name='Fried')   ##fri
    return render(request, "fri.html", {"items": items})


def sandwich(request):
    items = Menu.objects.filter(item_category__name='Sandwich')    ##sandwich
    return render(request, "sandwich.html", {"items": items})


def wrap(request):
    items = Menu.objects.filter(item_category__name='Wraps & Puffs')    ##wrap
    return render(request, "wrap.html", {"items": items})


def baked(request):
    items = Menu.objects.filter(item_category__name='Baked')    ##baked
    return render(request, "baked.html", {"items": items})    


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def success(request):
    return render(request, "home.html")


def offer(request):
    return render(request, "offer.html")


def  my_order(request):
    user_id = request.session.get('user_id')
 
    if not user_id:
        messages.error(request, "Please log in to view your order history.")
        return redirect('login')  # replace 'login' with your actual login url name
 
    try:
        user = Login.objects.get(id=user_id)
    except Login.DoesNotExist:
        request.session.flush()
        messages.error(request, "Session expired. Please log in again.")
        return redirect('login')
 
    orders = (
        Order.objects
        .filter(user=user)
        .prefetch_related('items')
        .order_by('-order_created_at')
    )
 
    return render(request, 'MyOrder.html', {'orders': orders})


def order_form(request, item_id):
    try:
        item = Menu.objects.get(id=item_id)
    except Menu.DoesNotExist:
        messages.error(request, "Item not found")
        return redirect('menu_page')

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address', '')

        if not all([name, email, phone]):
            messages.error(request, "Please fill in all required fields")
            return render(request, "order_form.html", {"item": item})

        customer, created = Customer.objects.get_or_create(
            cust_email=email,
            defaults={'cust_name': name, 'cust_phone': phone, 'cust_address': address}
        )

        Order.objects.create(
            customer_name=name,
            phone=phone,
            itemname=item
        )

        messages.success(request, f"Order placed successfully for {item.item_name}!")
        

    return render(request, "order_form.html", {"item": item})



##admin section--for admin use only

# def admin(request):
#     return render(request, "adminpanel.html")

# def dashboard(request):
#     return render(request, "dashboard.html")

## MENU section---page, update, delete, add

def Mmenu(request):
    item_obj=Menu.objects.all()    #fetch all data
    print(item_obj)
    context={                         #dictionary
        "items":item_obj                #key:value
    }
    return render(request,"managemenu.html",context)  

def menu_update(request, id):
    item_obj = Menu.objects.filter(id = id).first()
    item_categories = Category.objects.all()
    print(item_obj)

    if request.method == "POST":
        #emp_name = request.get.POST('emp_Name')
        item_name = request.POST['item_name']
        item_category = request.POST['item_category']
        item_description = request.POST['item_description']
        item_price = request.POST['item_price']
        item_available = request.POST['item_available']

        item_obj.item_name = item_name
        item_obj.item_category_id = item_category
        item_obj.item_description = item_description
        item_obj.item_price = item_price
        item_obj.item_available = item_available
        item_obj.save()

        return redirect("ManageMenu_page")

    context = {
        "item": item_obj,
        'categories': item_categories,
    }
    return render(request, "updatemenu.html", context)


def delete_menu(request,id):
    dele = Menu.objects.filter(id=id).first()
    dele.delete()
    return redirect('ManageMenu_page')

def menu_add(request):
    item_categories = Category.objects.all()

    if request.method == "POST":
        item_name = request.POST['item_name']
        item_category = request.POST['item_category']
        item_description = request.POST['item_description']
        item_price = request.POST['item_price']
        item_available = request.POST['item_available']

        Menu.objects.create(
            item_name=item_name,
            item_category_id=item_category,
            item_description=item_description,
            item_price=item_price,
            item_available=item_available
        )

        return redirect("ManageMenu_page")

    context = {
        "categories": item_categories
    }

    return render(request, "add_menu.html",context)



## CATEGORY section---page, update, delete, add

def category(request):
    cate_obj=Category.objects.all()    #fetch all data
    print(cate_obj)
    context={                         #dictionary
        "cates":cate_obj                #key:value
    }
    return render(request,"category.html",context) 

def cate_update(request, id):
    cate_obj = Category.objects.filter(id = id).first()
    print(cate_obj)

    if request.method == "POST":
        #emp_name = request.get.POST('emp_Name')
        name = request.POST['name']

        cate_obj.name = name
        cate_obj.save()

        return redirect("category_page")

    context = {
        "cate":cate_obj
    }
    return render(request, "updatecate.html", context)


def delete_cate(request,id):
    dele = Category.objects.filter(id=id).first()
    dele.delete()
    return redirect('category_page')


def category_add(request):

    if request.method == "POST":
        name = request.POST['name']

        Category.objects.create(
            name=name
        )

        return redirect("category_page")

    return render(request, "add_category.html")


## USER MANAGEMENT section-- page, update, delete, add

def user(request):
    login_obj=Login.objects.all()    #fetch all data
    print(login_obj)
    context={                         #dictionary
        "logins":login_obj                #key:value
    }
    return render(request,"adminuser.html",context) 

def user_update(request, id):
    login_obj = Login.objects.filter(id = id).first()
    print(login_obj)

    if request.method == "POST":
        #emp_name = request.get.POST('emp_Name')
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        login_obj.first_name = first_name
        login_obj.last_name = last_name
        login_obj.email = email
        login_obj.password = password
        login_obj.save()

        return redirect("user_page")

    context = {
        "login":login_obj
    }
    return render(request, "updateuser.html", context)


def delete_user(request,id):
    dele = Login.objects.filter(id=id).first()
    dele.delete()
    return redirect('user_page')


def user_add(request):

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        Login.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        return redirect("user_page")

    return render(request, "add_user.html")




## VIEW ORDER section-- page, update, delete


def order(request):
    ord_obj = Order.objects.all().prefetch_related('items')  # prefetch for efficiency
    context = {
        "ords": ord_obj
    }
    return render(request, "view_order.html", context)


def order_update(request, id):
    ord_obj = Order.objects.filter(id=id).first()

    if request.method == "POST":
        customer_name = request.POST['customer_name']
        phone = request.POST['phone']
        status = request.POST['status']

        ord_obj.customer_name = customer_name
        ord_obj.phone = phone
        ord_obj.status = status
        ord_obj.save()

        return redirect("order_page")

    context = {
        "ord": ord_obj,
    }
    return render(request, "update_order.html", context)



def delete_orders(request,id):
    dele = Order.objects.filter(id=id).first()
    dele.delete()
    return redirect('order_page')




from core.auth_utils import get_logged_in_user, login_required
from core.models import Cart, CartItem, OrderItem

def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart

@login_required
def add_to_cart(request, item_id):
    user = get_logged_in_user(request)
    menu_item = get_object_or_404(Menu, id=item_id)
    cart = get_or_create_cart(user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{menu_item.item_name} added to cart")
    return redirect(request.META.get('HTTP_REFERER', 'menu_page'))

@login_required
def view_cart(request):
    user = get_logged_in_user(request)
    cart = get_or_create_cart(user)
    return render(request, "cart.html", {"cart": cart})

@login_required
def update_cart_item(request, item_id):
    user = get_logged_in_user(request)
    cart = get_or_create_cart(user)
    cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)

    qty = int(request.POST.get('quantity', 1))
    if qty <= 0:
        cart_item.delete()
    else:
        cart_item.quantity = qty
        cart_item.save()
    return redirect('cart_page')

@login_required
def remove_from_cart(request, item_id):
    user = get_logged_in_user(request)
    cart = get_or_create_cart(user)
    CartItem.objects.filter(cart=cart, id=item_id).delete()
    return redirect('cart_page')



@login_required
def checkout(request):
    user = get_logged_in_user(request)
    cart = get_or_create_cart(user)

    if not cart.items.exists():
        messages.error(request, "Your cart is empty")
        return redirect('cart_page')

    if request.method == "POST":
        phone = request.POST.get('phone')
        address = request.POST.get('address', '')

        order = Order.objects.create(
            user=user,
            customer_name=f"{user.first_name} {user.last_name}",
            phone=phone,
            address=address,
            total_amount=cart.total_price(),
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order, menu_item=item.menu_item,
                item_name=item.menu_item.item_name,
                quantity=item.quantity,
                price_at_order=item.menu_item.item_price,
            )

        cart.items.all().delete()  # empty the cart, keep the Cart row for reuse
        request.session['pending_order_id'] = order.id
        return redirect('payment_page')

    return render(request, "checkout.html", {"cart": cart})


@login_required
def payment_page(request):
    order_id = request.session.get('pending_order_id')
    order = get_object_or_404(Order, id=order_id)
    return render(request, "payment.html", {"order": order})


@login_required
def confirm_payment(request, order_id):
    """Placeholder — swap in real gateway (Stripe/Razorpay) later."""
    order = get_object_or_404(Order, id=order_id)
    order.status = 'paid'
    order.payment_id = request.POST.get('payment_id', 'manual-confirm')
    order.save()
    request.session.pop('pending_order_id', None)
    messages.success(request, "Payment successful! Your order is confirmed.")
    return redirect('success_page')






# dashboard/views.py

from django.shortcuts import render
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta

from core.models import Order, OrderItem, Menu, Login


def dashboard(request):
    today = timezone.now().date()
    last_7_days = today - timedelta(days=7)
    last_30_days = today - timedelta(days=30)

    # ---- Top metric cards ----
    revenue_today = Order.objects.filter(
        order_created_at__date=today, status="completed"
    ).aggregate(total=Sum("total_amount"))["total"] or 0

    revenue_month = Order.objects.filter(
        order_created_at__date__gte=last_30_days, status="completed"
    ).aggregate(total=Sum("total_amount"))["total"] or 0

    orders_today = Order.objects.filter(order_created_at__date=today).count()
    pending_orders = Order.objects.filter(status="pending").count()

    total_customers = Login.objects.count()

    completed_orders = Order.objects.filter(status="completed")
    completed_count = completed_orders.count()
    avg_order_value = (
        (revenue_month / completed_count) if completed_count else 0
    )

    # ---- Revenue trend (last 7 days) ----
    revenue_trend_qs = (
        Order.objects.filter(order_created_at__date__gte=last_7_days, status="completed")
        .annotate(day=TruncDate("order_created_at"))
        .values("day")
        .annotate(total=Sum("total_amount"))
        .order_by("day")
    )
    revenue_trend_labels = [entry["day"].strftime("%b %d") for entry in revenue_trend_qs]
    revenue_trend_data = [float(entry["total"]) for entry in revenue_trend_qs]

    # ---- Best-selling menu items ----
    best_sellers = (
        OrderItem.objects.values("item_name")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-total_sold")[:5]
    )
    best_seller_labels = [item["item_name"] for item in best_sellers]
    best_seller_data = [item["total_sold"] for item in best_sellers]

    # ---- Order status breakdown ----
    status_breakdown = (
        Order.objects.values("status").annotate(count=Count("id")).order_by()
    )
    status_labels = [item["status"].title() for item in status_breakdown]
    status_data = [item["count"] for item in status_breakdown]

    # ---- Unavailable menu items ----
    unavailable_items = Menu.objects.filter(item_available=False)[:5]

    # ---- Recent orders ----
    recent_orders = Order.objects.select_related("user").order_by("-order_created_at")[:8]

    context = {
        "revenue_today": revenue_today,
        "revenue_month": revenue_month,
        "orders_today": orders_today,
        "pending_orders": pending_orders,
        "total_customers": total_customers,
        "avg_order_value": avg_order_value,
        "revenue_trend_labels": revenue_trend_labels,
        "revenue_trend_data": revenue_trend_data,
        "best_seller_labels": best_seller_labels,
        "best_seller_data": best_seller_data,
        "status_labels": status_labels,
        "status_data": status_data,
        "unavailable_items": unavailable_items,
        "recent_orders": recent_orders,
    }
    return render(request, "dashboard.html", context)