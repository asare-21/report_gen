from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'), 
    path('login/', views.login_, name='login'), 
    path('logout/', views.logout_, name='logout'), 
    path('register/', views.register, name='register'), 
    path('fm_general/', views.register, name='fm_general'), 
    path('fm_single/<str:id>', views.register, name='fm_single'), 
    path('tv_general/', views.register, name='tv_general'), 
    path('tv_single/<str:id>', views.register, name='tv_general'), 
]

handler404 = 'ease.views.notFound'
handler500 = 'ease.views.error500'
handler403 = 'ease.views.error403'