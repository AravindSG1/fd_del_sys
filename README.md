# 🍽️ Online Food Delivery System

An end-to-end food ordering and delivery platform built with **Python** and **Django**, supporting multiple user roles with role-based authentication and real-time order tracking.

---

## 🚀 Project Overview

This application enables customers to browse restaurants, place orders, and track them live. Restaurants receive and update orders, while delivery agents are automatically assigned to deliver the food. Admins verify restaurant accounts and manage the entire platform.

### User Roles

1. **Customer** — Places food orders and tracks status.
2. **Delivery Agent** — Delivers orders assigned by the system.
3. **Restaurant** — Prepares and manages incoming orders.
4. **Admin** — Verifies restaurant accounts, manages users (view/delete), and oversees the platform.

### Order Flow

- Customer places an order via the platform.
- The order appears on the corresponding restaurant’s dashboard.
- When the restaurant accepts the order, the system automatically assigns a delivery agent.
- All parties (customer, restaurant, delivery agent) see real-time status updates until delivery completion.

---

## 💻 Tech Stack

- **Backend:** Python, Django (with Django ORM)  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** SQLite (default with Django, can be swapped)  

---

## 🗂️ Project Structure 

online-food-delivery/  
├── manage.py  
├── db.sqlite3  
├── requirements.txt  
├── .gitignore  
├── accounts/  
├── adminpanel/  
├── core/  
├── customers/  
├── delivery/  
├── fd_del_sys/  
├── orders/  
├── payments/  
├── restaurants/  
├── media/  
├── static/  
└── templates/  


- **accounts/**: User authentication and profile management  
- **adminpanel/**: Admin dashboards and management tools  
- **core/**: Core pages like homepage and login  
- **customers/**: Customer-facing features and views  
- **delivery/**: Delivery agent functionalities  
- **fd_del_sys/**: Django project settings  
- **orders/**: Order processing logic  
- **payments/**: Payment processing and tracking  
- **restaurants/**: Restaurant menu and order management  
- **media/**: Uploaded profile and food images  
- **static/**: Static files (CSS, JS, images)  
- **templates/**: HTML templates organized by app  

---

## 🔑 Features

- Multi-role authentication and authorization with Django’s built-in user model extensions.  
- Real-time order status updates for customers, restaurants, and delivery agents.  
- Automatic delivery agent assignment upon restaurant order acceptance.  
- Fully functional cart system with add/remove/modify item capabilities.  
- Admin dashboard to verify restaurant accounts and manage users and orders.  
- Form validations and session handling to ensure secure and smooth user experience.  
- Clean, responsive frontend design with intuitive navigation.

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.x  
- Django 4.x  
- SQLite (default, no setup needed)

### Installation

1. Clone the repository:  
   ```
   git clone https://github.com/AravindSG1/fd_del_sys.git
   cd online-food-delivery
   ```
2. Install dependencies:  
    `pip install -r requirements.txt`

3. Apply migrations:  
    `python manage.py migrate`

4. Create a superuser (for admin access):  
    `python manage.py createsuperuser`

5. Run the development server:  
    `python manage.py runserver`

6. Open your browser at `http://127.0.0.1:8000/`