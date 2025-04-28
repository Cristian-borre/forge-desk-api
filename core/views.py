from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import Product, Quote, Customer
from .serializers import ProductSerializer, QuoteSerializer, CustomerSerializer
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

# Para manejar cotizaciones
class QuoteListCreateView(generics.ListCreateAPIView):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

# Para manejar clientes
class CustomerViewSets(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
