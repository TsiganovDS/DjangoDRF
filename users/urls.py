from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CustomTokenObtainPairView,
    PaymentViewSet,
    UserDelete,
    UserDetail,
    UserListView,
    UserProfileView,
    UserRegistrationView,
)

router = DefaultRouter()
router.register(r"users", UserProfileView)
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("api/users/", UserListView.as_view(), name="user-list"),
    path("api/users/register/", UserRegistrationView.as_view(), name="register"),
    path("api/users/<int:pk>/", UserDetail.as_view(), name="user-detail"),
    path("api/users/delete/", UserDelete.as_view(), name="user-delete"),
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("", include(router.urls)),
]
