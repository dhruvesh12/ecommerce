from django.conf.urls import url, include
from django.urls import path,include

from .views import *




urlpatterns = [
	path('register/',register,name='register'),
	path('login/',login,name='login'),
	path('logout/',logoutt,name='logoutt'),

    path('dash/<int:pk>/',homepage,name='homepage'),
    path('dash/<int:pk>/upload/',upload,name='upload'),
    path('dash/<int:pk>/restaurant_register/',restaurant_reg,name='restaurant_reg'),
    path('dash/<int:pk>/product_list/',product_list,name='product_list'),
    path('dash/<int:pk>/delete/',recipe_remove,name='recipe_remove'),
    path('dash/<int:pk>/edit/',recipe_edit,name='recipe_edit'),
    path('dash/<int:pk>/orders/',order_page,name='order_page'),
    path('dash/<int:pk>/create_orders/',create_order,name='create_order'),
    path('dash/<int:pk>/confirmed/',status,name='status'),

    path('error/',NoEntry,name='NoEntry'),

    
]