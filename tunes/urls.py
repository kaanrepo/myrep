from django.urls import path
from .views import home_view, tune_detail_view , tune_list_view

urlpatterns = [
    path('', home_view, name='home-view'),
    path('tunes/<str:username>/', tune_list_view, name='tunes-list-view'),
    path('tunes/<str:username>/<int:id>/', tune_detail_view, name='tunes-detail-view')
]
