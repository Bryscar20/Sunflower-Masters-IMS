import json
from django.db import OperationalError, connection
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer, Expense, InventoryItem, Inventory, SalesTransaction 
from .forms import ExpenseForm, InventoryItemForm, InventoryUpdateForm, SalesTransactionForm, CustomerForm

def base(request):
    recent_sales = SalesTransaction.objects.order_by('-date_sold')[:5]
    recent_expenses = Expense.objects.order_by('-date_incurred')[:5]
    inventory = Inventory.objects.all()
    context = {
        'recent_sales': recent_sales,
        'recent_expenses': recent_expenses,
        'inventory': inventory,
    }
    return render(request, 'base.html', context)

def dashboard(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM sun_seeds_salestransaction ORDER BY date_sold DESC LIMIT 5")
            columns = [col[0] for col in cursor.description]
            recent_sales = [dict(zip(columns, row)) for row in cursor.fetchall()]
            recent_sales_json = json.dumps({'labels': [sale['sunflower__name'] for sale in recent_sales],
                                            'data': [sale['quantity_sold'] for sale in recent_sales]})
    except OperationalError:
        recent_sales_json = json.dumps({'labels': [], 'data': []})

    recent_expenses = Expense.objects.order_by('-date_incurred')[:5]
    inventory = Inventory.objects.all()

    context = {
        'recent_sales': recent_sales,
        'recent_expenses': recent_expenses,
        'inventory': inventory,
        'recent_sales_json': recent_sales_json
    }
    return render(request, 'dashboard.html', context)

def customer_management(request):
    customers = Customer.objects.all()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_management')
    else:
        form = CustomerForm()
    return render(request, 'customer_management.html', {'customers': customers, 'form': form})


def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_management')
    else:
        form = CustomerForm(instance=customer)
    
    return render(request, 'edit_customer.html', {'form': form, 'customer': customer})

def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_management')
    
    return render(request, 'customer_delete.html', {'customer': customer})



def add_customer(request):
    return render(request, 'add_customer.html')


################################################################################

def expenses(request):
    recent_expenses = Expense.objects.order_by('-date_incurred')[:5]
    return render(request, 'expenses.html', {'recent_expenses': recent_expenses})

def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expenses')
    else:
        form = ExpenseForm()
    return render(request, 'expense_create.html', {'form': form})

def update_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expenses')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expense_update.html', {'form': form, 'expense': expense})

def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('expenses')
    return render(request, 'expense_delete.html', {'expense': expense})

def expense_detail(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    return render(request, 'expense_detail.html', {'expense': expense})

######################################################

def sales_dashboard(request):
    recent_sales = SalesTransaction.objects.all()[:5]
    return render(request, 'sales_dashboard.html', {'recent_sales': recent_sales})

def sales_transactions(request):
    recent_sales = SalesTransaction.objects.all()[:5]
    return render(request, 'sales_transactions.html', {'recent_sales': recent_sales})

def create_sale(request):
    if request.method == 'POST':
        form = SalesTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales_dashboard')
    else:
        form = SalesTransactionForm()
    return render(request, 'sale_create.html', {'form': form})


def sale_create(request):
    if request.method == 'POST':
        form = SalesTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales_dashboard')
    else:
        form = SalesTransactionForm()
    return render(request, 'sale_create.html', {'form': form})


def update_sale(request, pk):
    sale = get_object_or_404(SalesTransaction, pk=pk)
    if request.method == 'POST':
        form = SalesTransactionForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            return redirect('sales_dashboard')
    else:
        form = SalesTransactionForm(instance=sale)
    return render(request, 'sale_update.html', {'form': form})

def delete_sale(request, pk):
    sale = get_object_or_404(SalesTransaction, pk=pk)
    if request.method == 'POST':
        sale.delete()
        return redirect('sales_dashboard')
    return render(request, 'sale_delete.html', {'sale': sale})

def sale_detail(request, pk):
    sale = get_object_or_404(SalesTransaction, pk=pk)
    return render(request, 'sale_detail.html', {'sale': sale})


##################################################

@login_required
def sunflower_inventory(request):
    items = InventoryItem.objects.all()
    return render(request, 'sunflower_inventory.html', {'items': items})

@login_required
def inventory_detail(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    return render(request, 'inventory_detail.html', {'item': item})

@login_required
def inventory_create(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sunflower_inventory')
    else:
        form = InventoryItemForm()
    return render(request, 'inventory_create.html', {'form': form})

@login_required
def inventory_update(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        form = InventoryUpdateForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('sunflower_inventory')
    else:
        form = InventoryUpdateForm(instance=item)
    return render(request, 'inventory_update.html', {'form': form, 'item': item})

@login_required
def inventory_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('sunflower_inventory')
    return render(request, 'inventory_delete.html', {'item': item})


############################################
def user_profile(request):
    return render(request, 'user_profile.html')

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                error_message = "Failed to log in. Please try again."
                return render(request, 'registration_error.html', {'error_message': error_message})
    else:
        form = UserCreationForm()
    return render(request, 'user_register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = "Invalid username or password. Please try again."
            return render(request, 'user_login.html', {'error_message': error_message})
    else:
        return render(request, 'user_login.html')
