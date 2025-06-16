from django.urls import path
from . import views

urlpatterns = [
    path('scan_repo/', views.receive_repo, name='scan_repo'),
]
