from django.urls import path
from .views import login_logout_view, register_user_view, user_profile_view, user_profile_update_view

urlpatterns = [
    path('login/', login_logout_view, name='login-view'),
    path('logout/', login_logout_view, name='logout-view'),
    path('register/', register_user_view, name='user-register-view'),
    path('profile/<int:pk>/', user_profile_view, name='profile-view'),
    path('profile/update/<int:pk>/', user_profile_update_view, name='profile-update-view')
]