from django.urls import path
from .views import UserCreateView, LoginView

urlpatterns = [
    # path('login/', GenerateTokenView.as_view(), name='login'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
