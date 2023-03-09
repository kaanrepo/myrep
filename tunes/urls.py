from django.urls import path
from .views import home_view, usertune_detail_view , usertune_list_view, usertune_list_hx_view, tune_create_view, tune_update_view,usertune_pdf_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home_view, name='home-view'),
    path('hx/', home_view, name='home-hx-view'),
    path('hx/tunes/<int:pk>/', usertune_list_hx_view, name='hx-tunes-list-view'),
    path('tunes/<int:pk>/', usertune_list_view, name='tunes-list-view'),
    path('tunes/<int:pk>/<int:id>/', usertune_detail_view, name='tunes-detail-view'),
    path('tunes/add/',tune_create_view, name='tunes-create-view'),
    path('tunes/update/<int:pk>/<int:id>/', tune_update_view, name='tunes-update-view'),
    path('tunes/<int:pk>/<int:id>/sheet/', usertune_pdf_view, name='usertune-sheet-view'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
