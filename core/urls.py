from django.urls import path, include
from core.views import CustomerViewSets, ProductViewsets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('customers', CustomerViewSets, basename='customer')
router.register('products', ProductViewsets, basename='inventory')

urlpatterns = [
    path('', include(router.urls)),
]