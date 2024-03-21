from django.contrib import admin
from django.urls import path, include
from sun_seeds.views import base, create_expense, create_sale, sale_create, customer_delete, customer_management, delete_expense, delete_sale, edit_customer, expense_detail, expenses, sale_detail, sales_dashboard, update_expense, update_sale, user_login, user_register, sales_transactions, sunflower_inventory, user_profile, dashboard, add_customer, inventory_detail, inventory_create, inventory_update, inventory_delete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Include auth URLs
    # Add other app-specific URLs here
    path('', base, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    
    path('customer-management/', customer_management, name='customer_management'),
    path('add-customer/', add_customer, name='add_customer'),
    path('edit-customer/<int:pk>/', edit_customer, name='edit_customer'), 
    path('delete-customer/<int:pk>/', customer_delete, name='customer_delete'), 
    
    path('sales-transactions/', sales_transactions, name='sales_transactions'),
    path('sales_dashboard/', sales_dashboard, name='sales_dashboard'),
    path('sale_create/', create_sale, name='sale_create'),
    path('update_sale/<int:pk>/', update_sale, name='update_sale'),
    path('delete_sale/<int:pk>/', delete_sale, name='delete_sale'),
    path('sale_detail/<int:pk>/', sale_detail, name='sale_detail'),

    path('expenses/', expenses, name='expenses'),
    path('expense/create/', create_expense, name='expense_create'),
    path('expense/<int:pk>/update/', update_expense, name='expense_update'),
    path('expense/<int:pk>/delete/',delete_expense, name='expense_delete'),
    path('expense/<int:pk>/', expense_detail, name='expense_detail'),

    path('sunflower-inventory/', sunflower_inventory, name='sunflower_inventory'),
    path('item/<int:pk>/', inventory_detail, name='inventory_detail'),
    path('item/new/', inventory_create, name='inventory_create'),
    path('item/<int:pk>/edit/', inventory_update, name='inventory_update'),
    path('item/<int:pk>/delete/', inventory_delete, name='inventory_delete'),

    path('user-profile/', user_profile, name='user_profile'),
    path('user-register/', user_register, name='user_register'),
    path('user-login/', user_login, name='user_login'),
]
