
from django.urls import path
from . import views


urlpatterns = [
    path('items/', views.ItemListView.as_view(), name='items'),
    path('item/<int:pk>', views.ItemDetailView.as_view(), name='item-detail'),
    
]

urlpatterns += [
    path('item/create/', views.ItemCreate.as_view(), name='item-create'),
 
]

#   path('item/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),   path('item/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),