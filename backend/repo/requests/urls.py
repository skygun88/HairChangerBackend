from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.swapRequest, name='request'),
    path('update/', views.update, name='update'),
    path('cancel/', views.cancel, name='cancel'),
    path('download/', views.download, name='download'),
    path('test/', views.test, name='test'),
]