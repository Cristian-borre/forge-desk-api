from rest_framework import serializers
from .models import Product, Quote, Category, Customer

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class QuoteSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    class Meta:
        model = Quote
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    last_quote_date = serializers.DateTimeField(read_only=True)
    last_quote_status = serializers.CharField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone', 'address', 'created_at', 'last_quote_date', 'last_quote_status']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
