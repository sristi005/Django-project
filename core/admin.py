from django.contrib import admin
from core.models import Customer, Category, Menu, Order, OrderItem, Login, Cart, CartItem


@admin.register(Login)
class login_details(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
        'password',
    ]


@admin.register(Customer)
class customer_details(admin.ModelAdmin):
    list_display = [
        'id',
        'cust_name',
        'cust_email',
        'cust_phone',
        'cust_address',
        'cust_created_at',
    ]


@admin.register(Category)
class category_details(admin.ModelAdmin):
    list_display = [
        'name'
    ]


@admin.register(Menu)
class menu_details(admin.ModelAdmin):
    list_display = [
        'id',
        'item_name',
        'item_category',
        'item_description',
        'item_price',
        'item_available',
    ]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class order_details(admin.ModelAdmin):
    list_display = [
        'id',
        'customer_name',
        'phone',
        'total_amount',
        'status',
        'order_created_at',
    ]
    inlines = [OrderItemInline]


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class cart_details(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'created_at',
    ]
    inlines = [CartItemInline]