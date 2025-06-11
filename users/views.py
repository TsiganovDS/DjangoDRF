from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserProfileSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = []


class UserDelete(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserProfileUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
