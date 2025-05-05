from django.shortcuts import render
from rest_framework import viewsets, serializers
from .models import Product, Quote, Customer, Order, Component
from .serializers import ProductSerializer, QuoteSerializer, CustomerSerializer, ComponentSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Max, F, Subquery, OuterRef

# Create your views here.

# Para manejar productos
class ProductViewsets(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

# Para manejar componentes
class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

# Para manejar clientes
class CustomerViewSets(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    swagger_tags = ['Customers']

    def get_queryset(self):
        queryset = Customer.objects.all()

        queryset = queryset.annotate(
            last_quote_date=Max('quote__created_at')
        )

        queryset = queryset.annotate(
            last_quote_status=Subquery(
                Quote.objects.filter(
                    customer=OuterRef('pk')
                ).order_by('-created_at').values('status')[:1]
            )
        )

        return queryset
    
# Para manejar cotizaciones
class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        if not instance.check_stock():
            raise serializers.ValidationError("No hay stock suficiente para esta cotización.")

# Para manejar pedidos
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.create_order()  # Descuenta componentes
