from django.contrib import admin
from .models import Customer, Component, Product, ProductComponent, Quote, Order

# Registro de Cliente
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'address', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)

admin.site.register(Customer, CustomerAdmin)

# Registro de Componente
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_of_measure', 'stock', 'price_per_unit', 'created_at')
    search_fields = ('name',)
    list_filter = ('unit_of_measure',)

admin.site.register(Component, ComponentAdmin)

# Registro de Producto
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_unit', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

admin.site.register(Product, ProductAdmin)

# Registro de Relación Producto-Componentes
class ProductComponentAdmin(admin.ModelAdmin):
    list_display = ('product', 'component')
    search_fields = ('product__name', 'component__name')

admin.site.register(ProductComponent, ProductComponentAdmin)

# Registro de Cotización
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'width', 'height', 'quantity', 'price', 'status', 'created_at')
    search_fields = ('customer__name', 'product__name', 'status')
    list_filter = ('status', 'created_at')

admin.site.register(Quote, QuoteAdmin)

# Registro de Pedido
class OrderAdmin(admin.ModelAdmin):
    list_display = ('quote', 'order_date', 'status')
    search_fields = ('quote__customer__name', 'quote__product__name', 'status')
    list_filter = ('status',)

admin.site.register(Order, OrderAdmin)
