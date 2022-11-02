from django.urls import path
from . import views


urlpatterns = [
    path('category/', views.recommand_category),
    path('category', views.recommand_category),
]
