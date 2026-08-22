from django.db import models


class Login(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email


class Customer(models.Model):
    cust_name = models.CharField(max_length=20)
    cust_email = models.EmailField()
    cust_phone = models.CharField(max_length=15)
    cust_address = models.TextField()
    cust_created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cust_name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    item_name = models.CharField(max_length=50)
    item_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    item_description = models.TextField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.item_name} ({self.item_category.name})"


class Cart(models.Model):
    user = models.OneToOneField(Login, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.subtotal() for item in self.items.all())

    def total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'menu_item')

    def subtotal(self):
        return self.menu_item.item_price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('preparing', 'Preparing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='orders', null=True)
    customer_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15)
    address = models.TextField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    order_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True)
    item_name = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=1)
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.price_at_order * self.quantity