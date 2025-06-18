from django.urls import path

from .views import UserCreate, UserDelete, UserDetail, UserList, UserProfileUpdate

app_name = "users"

urlpatterns = [
    path("users/", UserList.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetail.as_view(), name="user_detail"),
    path("users/create/", UserCreate.as_view(), name="user_create"),
    path("profile/", UserProfileUpdate.as_view(), name="user_profile_update"),
    path("profile/delete/", UserDelete.as_view(), name="user_delete"),
]
