
from django.urls import path
from . import views
from .views import MyTokenObtainPairView , get_routes

from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView,
)

urlpatterns = [
    path('profile/', views.get_profile),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('changePassword/', views.change_password, name='change_password' ),
    path ('createUser/', views.createUser, name='create_user' ),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('search_items/', views.search_items, name='search_items'),
    path('getItems/' , views.items_for_sale , name ="get_items"),
    path('add_item/', views.add_item, name='add_item'),
    path('items/on_sale/', views.items_on_sale, name='items_on_sale'),
    path('items/sold/', views.sold_items, name='sold_items'),
    path('items/purchased/', views.purchased_items, name='purchased_items'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('items_to_purchase/', views.items_to_purchase, name='items_to_purchase'),
    path('pay/', views.pay_for_items, name='pay_for_items'),
    path('edit_item_price/', views.edit_item_price, name='edit_item_price'),
     path('item_details/', views.item_details, name='item_details'),
    path("", get_routes, name="all_routes" )
]
