
# CAFE HUT

A full-stack cafe ordering website developed using **Django** that allows users to browse the menu, add items to a cart, place orders, and view their order history. The project also includes an **admin section** for managing and monitoring customer orders.


## Project Overview
The CAFE HUT Website provides a simple and user-friendly platform for customers to order cafe items online.

Users can create an account, log in, explore different menu categories, add multiple items to their cart, adjust quantites, proceed to checkout and view their previous orders.

The project demonstrate the implementation of **Django, database management, user authentication, CRUD operations and dynamic web pages**.
## Features

### User Features

- User registration and login
- Secure user authentication
- Browse **CAFE HUT** menu
- View different food categories
- Add items to cart
- Increase or decrease item quantity
- Automatic price calculation based quantity
- Checkout and order placement
- View previous orders
- Logout functionality

### Shopping Cart

- Add multiple products to the cart
- Update product quantities
- Remove items from the cart
- Automatically calculate the total price
- Proceed to checkout

### Admin Features

- Admin login
- View customer orders
- Monitor placed orders
- Manage website data through the Django admin panel

### Other Pages

- Home
- Menu
- My Order
- About
- Contact
- Cart



## Technologies Used

**Frontend:** HTML, CSS

**Backend:** Python, Django

**Database:** MySQL

**Authentication:** Django Authentication System

**Development Environment:** VS Code


## Installation

### 1. Clone the Repository

```bash
  git Clone
  https://github.com/sristi005/Django-project.git
```
### 2. Clone the Repository

```bash
  cd Django-project
```
### 3. Create a Virtual Environment

```bash
  python -m venv venv
```
### 4. Activate the Virtual Environment

```bash
  venv\Scripts\activate
```
### 5. Install Dependencies

```bash
  pip install django
```
### 6. Apply Database Migrations

```bash
  python manage.py makemigrations
  python manage.py migrate
```
### 7. Create an Admin/Superuser 

```bash
  python manage.py createsuperuser
```
 Follow the instructions in the terminal to create the admin account.

### 8. Run the Development Server

```bash
  python manage.py runserver 
```    
Open the local server in your browser:
```bash
http://127.0.0.1:8000/
```
## Database

The project uses **MySQL** as the database management system. Django ORM is used to manage user accounts, menu items, cart details, and customer orders efficiently. 
## What I Learned

* Building dynamic web applications using Django.
* Connecting Django with a MySQL database.
* Implementation user authentication and authorization.
* Performing CRUD operation.
* Managing customer orders using Django ORM.
* Designing a responsive and user-friendly website.


## Future Improvements

* Online payment gateway integration.
* Order tracking System.
* Customer profile management.
* Fully responsive mobile-friendly design.
* Product search and filtering. 
## Developer
### Sristi Biswas
B.Tech in Computer Science & Engineering
Interested in Web Development and Software Development.
## License

This project is created for educational and portfolio purposes.

