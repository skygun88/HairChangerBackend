from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('upgrade/', views.upgrade, name='upgrade'),
    path('downgrade/', views.downgrade, name='downgrade'),
    path('set/', views.setProfile, name='setProfile'),
    path('reset/', views.resetProfile, name='resetProfile'),
]