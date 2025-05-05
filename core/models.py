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

# Componente (Material o parte que compone un producto)
class Component(models.Model):
    name = models.CharField(max_length=255)
    unit_of_measure = models.CharField(max_length=50, default='unit')  # Puede ser "kg", "pieza", "metro", etc.
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Stock disponible
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)  # Precio por unidad
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Producto
class Product(models.Model):
    name = models.CharField(max_length=255)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)  # Precio por unidad del producto
    components = models.ManyToManyField(Component, through='ProductComponent')  # Relación con los componentes
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_components(self):
        return Component.objects.filter(productcomponent__product=self)

# Relación Producto-Componentes (especificando cantidad de cada componente por producto)
class ProductComponent(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity_needed} de {self.component.name} para {self.product.name}"

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
    quantity = models.PositiveIntegerField(default=1)  # Cantidad de productos
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio por el total de la cotización
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='quotes_pdfs/', blank=True, null=True)  # Ruta al PDF generado

    def __str__(self):
        return f"Quote #{self.id} - {self.customer.name}"
    
    def calculate_components(self):
        components_needed = {}

        for product_component in self.product.productcomponent_set.all():
            component = product_component.component
            quantity_needed = self.quantity  # Cantidad de productos solicitados
            
            if component.unit_of_measure == 'm²':
                quantity_needed *= self.width * self.height
            elif component.unit_of_measure == 'm':
                quantity_needed *= (self.width * 2 + self.height * 2)

            components_needed[component] = quantity_needed

        return components_needed

    def check_stock(self):
        components_needed = self.calculate_components()
        for component, needed in components_needed.items():
            if component.stock < needed:
                return False  # No hay suficiente stock para cumplir con la cotización
        return True

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

    def create_order(self):
        # Cuando se crea un pedido, descontamos el stock de los componentes
        for product_component in self.quote.product.productcomponent_set.all():
            component = product_component.component
            quantity_used = product_component.quantity_needed * self.quote.quantity
            component.stock -= quantity_used
            component.save()
