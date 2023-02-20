from django.urls import path
from .views import login_logout_view, register_user_view

urlpatterns = [
    path('login/', login_logout_view, name='login-view'),
    path('logout/', login_logout_view, name='logout-view'),
    path('register/', register_user_view, name='user-register-view')
]