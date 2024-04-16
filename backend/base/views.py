from django.shortcuts import render
from django.contrib.auth.models import User
from base.models import Item
from django.http import HttpResponse , JsonResponse
from django.views import generic
import random

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
                 item = Item.objects.create(title=title , description=description , price=price , seller=user)
                 
        
        return HttpResponse("Test users successfully created.")
    except Exception as e:
        return HttpResponse(f"Failed to create test users: {str(e)}", status=500)


class ItemListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Item
    paginate_by = 10


