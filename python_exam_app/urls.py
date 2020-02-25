from django.urls import path
from . import views	

urlpatterns = [
    path('', views.index),
    path('users', views.createUser),
    path('login', views.login),
    path('homepage', views.homepage),
    path('logged_out', views.logged_out),
    path('createQuote', views.createQuote),
    path('likeQuote/<int:quote_id>', views.likeQuote),
    path('unlikeQuote/<int:quote_id>', views.unlikeQuote),
    path('delete/<int:quote_id>', views.deleteQuote),
    path('profile/<int:user_id>', views.profile),
    path('editPage/', views.editPage),
    path('updateInfo', views.updateInfo),
]