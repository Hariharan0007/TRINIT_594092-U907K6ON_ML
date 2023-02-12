from django.urls import path

from . import views

urlpatterns=[
    path('',views.login,name='login'),
    path('predict/',views.crop_predict,name='crop_predict'),
]

