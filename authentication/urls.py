from django.urls import path
from .views import (UserRegistrationView, UserLoginView, UserLogoutView, UserDetailsView,
                    UserUpdateView, UserPasswordAPIView)


urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name='user-logout'),
    path("user/", UserDetailsView.as_view(), name='user-details'),
    path("update/", UserUpdateView.as_view(), name='user-update'),
    path("change-password/", UserPasswordAPIView.as_view(), name="change-password")
]
