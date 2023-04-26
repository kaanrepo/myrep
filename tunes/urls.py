from django.urls import path
from .views import (home_view, usertune_detail_view , usertune_list_view, usertune_list_hx_view, tune_create_view, tune_update_view, usertune_pdf_view, public_usertune_view, usertune_lists_view, usertune_lists_detail_view, usertune_list_create_view, delete_objects_view, usertune_list_update_view,copy_tune_view)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home_view, name='home-view'),
    path('tunes/library', public_usertune_view, name='public-usertune-view'),
    path('tunes/hx/', public_usertune_view, name='public-usertune-hx-view'),
    path('hx/tunes/<int:pk>/', usertune_list_hx_view, name='hx-tunes-list-view'),
    path('tunes/<int:pk>/', usertune_list_view, name='tunes-list-view'),
    path('tunes/<int:pk>/<int:id>/', usertune_detail_view, name='tunes-detail-view'),
    path('tunes/list/<int:pk>/', usertune_lists_view, name='usertune-lists-view'),
    path('tunes/hx/list/<int:pk>/', usertune_lists_view, name='usertune-lists-hx-view'),
    path('tunes/list/<int:pk>/<int:id>/', usertune_lists_detail_view, name='usertune-lists-detail-view'),
    path('tunes/list/create/',usertune_list_create_view, name='list-create-view'),
    path('tunes/list/<int:pk>/<int:id>/update/',usertune_list_update_view, name='list-update-view'),
    path('tunes/add/',tune_create_view, name='tunes-create-view'),
    path('tunes/copy/<int:pk>/', copy_tune_view, name='tunes-copy-view'),
    path('tunes/update/<int:pk>/<int:id>/', tune_update_view, name='tunes-update-view'),
    path('tunes/<int:pk>/<int:id>/sheet/', usertune_pdf_view, name='usertune-sheet-view'),
    path('<str:model>/<int:pk>/delete/', delete_objects_view, name='delete-objects-view'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
