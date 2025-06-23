from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import PaymentViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('lms/', include('lms.urls')),
    path('users/', include('users.urls')),
]
