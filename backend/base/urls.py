
from django.urls import path
from . import views


urlpatterns = [
    path('', views.shopPage, name='shop_page'),
    path('items/', views.ItemListView.as_view(), name='items'),
    path('item/<int:pk>', views.ItemDetailView.as_view(), name='item-detail'),
    path('item/edit-item-price/<str:title>/', views.edit_item_price, name='edit_item_price'),
    
]

urlpatterns += [
    path('item/create/', views.ItemCreate.as_view(), name='item-create'),
    path('add-item/', views.add_item, name='add_item'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
     path('checkout/', views.checkout, name='checkout'),
     path('cart/', views.view_cart, name='cart'),
     path('my-items/', views.view_my_items, name='my_items'),
 
]
 
    


urlpatterns += [
    path('search/', views.ItemSearchListView.as_view(), name='item-search'),
 
]


#   path('item/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),   path('item/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),