from rest_framework import serializers
from .models import Product, Quote, Customer, Component, Order, ProductComponent


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    component_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    components = ComponentSerializer(source='get_components', many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price_per_unit', 'component_ids', 'components', 'created_at']

    def create(self, validated_data):
        component_ids = validated_data.pop('component_ids', [])
        product = Product.objects.create(**validated_data)

        for comp_id in component_ids:
            try:
                component = Component.objects.get(pk=comp_id)
                ProductComponent.objects.create(product=product, component=component)
            except Component.DoesNotExist:
                raise serializers.ValidationError(f"Component with ID {comp_id} not found")

        return product

    def update(self, instance, validated_data):
        component_ids = validated_data.pop('component_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if component_ids is not None:
            ProductComponent.objects.filter(product=instance).delete()

            for comp_id in component_ids:
                component = Component.objects.get(pk=comp_id)
                ProductComponent.objects.create(product=instance, component=component)

        return instance

class QuoteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = Quote
        fields = ['id', 'customer', 'product', 'product_id', 'width', 'height', 'quantity', 'price', 'status', 'created_at', 'pdf']

class CustomerSerializer(serializers.ModelSerializer):
    last_quote_date = serializers.DateTimeField(read_only=True)
    last_quote_status = serializers.CharField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone', 'address', 'created_at', 'last_quote_date', 'last_quote_status']

class OrderSerializer(serializers.ModelSerializer):
    quote = QuoteSerializer(read_only=True)
    quote_id = serializers.PrimaryKeyRelatedField(queryset=Quote.objects.all(), source='quote', write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'quote', 'quote_id', 'order_date', 'status']
