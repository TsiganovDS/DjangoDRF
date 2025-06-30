import django_filters
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework import generics, permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse_lazy
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Payment, User
from .serializers import (
    PaymentSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
)


class UserBaseView:
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer


class UserDetail(UserBaseView, generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]


class UserCreate(UserBaseView, generics.CreateAPIView):
    permission_classes = []


class UserDelete(UserBaseView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserProfileView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileUpdate(UserBaseView, generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class PaymentFilter(django_filters.FilterSet):
    class Meta:
        model = Payment
        fields = ["payment_date", "amount"]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = PaymentFilter
    ordering_fields = ["payment_date"]
    ordering = ["payment_date"]


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    template_name = "lms/register.html"
    success_url = reverse_lazy('lms:index')
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class UserListView(UserBaseView, generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]


class UserDetailView(UserBaseView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
