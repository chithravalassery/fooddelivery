from django.urls import path


from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.restaurant_list, name='restaurant_list'),
    path('menu/<int:restaurant_id>/', views.menu_items, name='menu_items'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:menu_item_id>/', views.add_to_cart, name='add_to_cart'),
    path('accounts/login/', LoginView.as_view(), name='login'), 
    path('logout/', views.logout_view, name="logout"),  
    path('accounts/sign_up/', views.sign_up, name='register'),
]

