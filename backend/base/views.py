from django.shortcuts import render
from django.contrib.auth.models import User
from base.models import Item
from django.http import HttpResponse , JsonResponse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
import random
import datetime
MAX_ITEM_PRICE = 100
MIN_ITEM_PRICE = 0

# Create your views here.


def homePage (request):

    context = {}
    return render(request, "base/index.html", context)




def generate_test_users(request):
    try:
        # Delete existing test users if they already exist
        User.objects.filter(username__startswith='testuser').delete()
        
        # Generate new test users
        for i in range(1, 7):
            username = f'testuser{i}'
            email = f'{username}@shop.aa'
            password = f'pass{i}'
            user = User.objects.create_user(username=username, email=email, password=password)
            
            if i <= 3 :
                 title = f'title{i}'
                 description = f'description{i}'
                 price = random.randint(MIN_ITEM_PRICE , MAX_ITEM_PRICE )
                 date_added = datetime.datetime.now()
                 item = Item.objects.create(title=title , description=description , price=price , seller=user , date_added = date_added)
                 
        
        return HttpResponse("Test users successfully created.")
    except Exception as e:
        return HttpResponse(f"Failed to create test users: {str(e)}", status=500)


class ItemDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Item



class ItemListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Item
    paginate_by = 10
    
    def get_queryset(self):
        
        return Item.objects.all().filter(is_sold=False)





class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html" 




class ItemCreate(generic.edit.CreateView):
    model = Item
    fields = ['description', 'image', 'price', 'seller' , 'date_added']
    initial = {'date_of_death': '11/11/2023'}
    permission_required = 'base.add_ item'
