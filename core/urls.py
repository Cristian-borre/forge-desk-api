from django.urls import path, include
from core.views import CustomerViewSets, ProductViewsets, QuoteViewSet, OrderViewSet, ComponentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('customers', CustomerViewSets, basename='customers')
router.register('products', ProductViewsets, basename='products')
router.register('quotes', QuoteViewSet, basename='quotes')
router.register('orders', OrderViewSet, basename='orders')
router.register('components', ComponentViewSet, basename='components')

urlpatterns = [
    path('', include(router.urls)),
]