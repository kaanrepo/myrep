from django.urls import path
from .views import home_view, usertune_detail_view , usertune_list_view, tune_create_view, tune_update_view

urlpatterns = [
    path('', home_view, name='home-view'),
    path('tunes/<int:pk>/', usertune_list_view, name='tunes-list-view'),
    path('tunes/<int:pk>/<int:id>/', usertune_detail_view, name='tunes-detail-view'),
    path('tunes/add/',tune_create_view, name='tunes-create-view'),
    path('tunes/update/<int:pk>/<int:id>/',tune_update_view, name='tunes-update-view')
]
