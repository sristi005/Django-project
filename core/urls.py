from django.urls import path
from core.views import (
    about,home,contact,offer,menu,
    Signin,signin_page,
    coffee,fri,sandwich,wrap,baked,
    success,
    order_form,
    my_order,
    dashboard,Mmenu,menu_update,category,cate_update,user,user_update,order,order_update,
    delete_menu,delete_cate,delete_user,delete_orders,
    category_add,menu_add,user_add,

    logout_view,add_to_cart,view_cart,update_cart_item,remove_from_cart,
    checkout,payment_page,confirm_payment
)


##for image in html page
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns=[
    path('signin',signin_page,name="signin_page"),
    path('login',Signin,name="login_page"),
    path('about',about,name="about_page"),
    path('home',home,name="home_page"),
    path('contact',contact,name="contact_page"),
    path('success',success,name="success_page"),
    path('menu',menu,name="menu_page"),
    path('offer',offer,name="offer_page"),
    path('myorder',my_order,name="order_history_page"),

##for menu in html page

    path('coffee',coffee,name="coffee_page"),
    path('fri',fri,name="fri_page"),
    path('sandwich',sandwich,name="sandwich_page"),
    path('wrap',wrap,name="wrap_page"),
    path('baked',baked,name="baked_page"),

    path('order_form/<int:item_id>/', order_form, name="order_form"),


##For admin panel

    # path('adminpanel',admin,name="admin_page"),
    path('dashboard',dashboard,name="dashboard_page"),

    path('manageMenu',Mmenu,name="ManageMenu_page"),
    path("update/<int:id>", menu_update, name="menu_update"),   ##for update manageMenu from admin panel

    path('category',category,name="category_page"),
    path("update1/<int:id>", cate_update, name="cate_update"),

    path('user',user,name="user_page"),
    path("update2/<int:id>", user_update, name="user_update"),

    path('adminorder',order,name="order_page"),
    path("update3/<int:id>", order_update, name="order_update"),

## for deleting menu from admin panel manage menu section
    path('delete/<int:id>',delete_menu,name="menu_delete"),  

## for deleting category from admin panel category section    
    path('delete1/<int:id>',delete_cate,name="cate_delete"),

## for deleting login users     
    path('delete2/<int:id>',delete_user,name="user_delete"),

## for deleting orders from admin panel
    path('delete3/<int:id>',delete_orders,name="order_delete"),



    path('addcategory',category_add,name="category_add"),
    path('addmenu',menu_add,name="menu_add"),
    path('adduser',user_add,name="user_add"),




path('logout', logout_view, name="logout_page"),
path('cart/add/<int:item_id>/', add_to_cart, name="add_to_cart"),
path('cart/', view_cart, name="cart_page"),
path('cart/update/<int:item_id>/', update_cart_item, name="update_cart_item"),
path('cart/remove/<int:item_id>/', remove_from_cart, name="remove_from_cart"),
path('checkout/', checkout, name="checkout_page"),
path('payment/', payment_page, name="payment_page"),
path('payment/confirm/<int:order_id>/', confirm_payment, name="confirm_payment"),
]





