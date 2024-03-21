from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Sunflower(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'sun_seeds'


class Inventory(models.Model):
    sunflower = models.OneToOneField(Sunflower, on_delete=models.CASCADE)
    quantity_available = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Inventory for {self.sunflower.name}"

    class Meta:
        app_label = 'sun_seeds'


class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('inventory_detail', kwargs={'pk': self.pk})

    class Meta:
        app_label = 'sun_seeds'


class SalesTransaction(models.Model):
    sunflower = models.ForeignKey(Sunflower, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_sold = models.DateField()

    def __str__(self):
        return f"Sales of {self.sunflower.name}"

    class Meta:
        app_label = 'sun_seeds'

    @classmethod
    def calculate_total_price(cls):
        """
        Calculate the total price of the transaction based on quantity sold and unit price of the product.
        """
        cls.total_price = cls.sunflower.unit_price * cls.quantity_sold

    def update_inventory(self):
        """
        Update inventory levels after a sales transaction by decrementing the quantity sold from available inventory.
        """
        inventory = Inventory.objects.get(sunflower=self.sunflower)
        inventory.quantity_available -= self.quantity_sold
        inventory.save()

    @classmethod
    def get_recent_sales(cls, limit=5):
        """
        Retrieve recent sales transactions.
        """
        return cls.objects.order_by('-date_sold')[:limit]


@receiver(post_save, sender=SalesTransaction)
def update_inventory(sender, instance, created, **kwargs):
    if created:
        instance.update_inventory()


class Expense(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_incurred = models.DateField()

    def __str__(self):
        return self.description

    class Meta:
        app_label = 'sun_seeds'
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

    class Meta:
        app_label = 'sun_seeds'


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        app_label = 'sun_seeds'


class PipelineStage(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField()  # To maintain the order of stages
    
    def __str__(self):
        return self.name

    class Meta:
        app_label = 'sun_seeds'
        ordering = ['order']


class PipelineEntry(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    stage = models.ForeignKey(PipelineStage, on_delete=models.CASCADE)
    entered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer} - {self.stage}"

    class Meta:
        app_label = 'sun_seeds'
        ordering = ['-entered_at']


class Interaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    notes = models.TextField()
    interaction_type = models.CharField(max_length=50)
    interaction_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.customer} - {self.interaction_type}"

    class Meta:
        app_label = 'sun_seeds'
        ordering = ['-interaction_date']


class Task(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

    class Meta:
        app_label = 'sun_seeds'
        ordering = ['due_date']


class PipelineAnalytics(models.Model):
    stage = models.ForeignKey(PipelineStage, on_delete=models.CASCADE)
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.stage} - {self.month}/{self.year}"

    class Meta:
        app_label = 'sun_seeds'
        unique_together = ['stage', 'month', 'year']


class Purchase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sunflower = models.ForeignKey(Sunflower, on_delete=models.CASCADE)
    quantity_purchased = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_purchased = models.DateField()
    
    def __str__(self):
        return f"Purchase of {self.sunflower.name} by {self.customer.name}"

    class Meta:
        app_label = 'sun_seeds'


class CustomerPipeline(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    stage = models.CharField(max_length=50)
    notes = models.TextField()
    last_contact_date = models.DateField()
    next_action_date = models.DateField()
    
    def __str__(self):
        return f"{self.customer} - {self.stage}"

    class Meta:
        app_label = 'sun_seeds'
