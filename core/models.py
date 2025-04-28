from django.db import models

# Create your models here.

from django.db import models

# Cliente
class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Categoria
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Producto
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    unit_of_measure = models.CharField(max_length=50, default='unit')
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Cotización
class Quote(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    width = models.DecimalField(max_digits=10, decimal_places=2)  # Ancho en metros
    height = models.DecimalField(max_digits=10, decimal_places=2)  # Alto en metros
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='quotes_pdfs/', blank=True, null=True)  # Ruta al PDF generado

    def __str__(self):
        return f"Quote #{self.id} - {self.customer.name}"

# Pedido
class Order(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
    ]

    quote = models.OneToOneField(Quote, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')

    def __str__(self):
        return f"Order #{self.id} - {self.quote.customer.name}"
