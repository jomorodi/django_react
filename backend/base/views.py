from django.shortcuts import render
from django.contrib.auth.models import User
from base.models import Item
from django.http import HttpResponse , JsonResponse

# Create your views here.


def homePage (request):

    context = {}
    return render(request, "base/index.html", context)


def populate(request):
    # clearing the DB
    User.objects.all().delete()
    Item.objects.all().delete()

    #populating with no_u users and no_c cards each
    no_u = 3
    no_c = 2
    try:
        color_list = ['red', 'green', 'blue', 'pink', 'black', 'orange']
        for n in range(no_u):
            user = User.objects.create_user("user{}".format(n), "user{}@myserver.com".format(n), "pass{}".format(n))
            user.save()

            for i in range(no_c):
                item = Card(color=random.choice(color_list), owner=user)
                item.save()
        message = "populated with {} users and {} cards each".format(no_u, no_c)
    except Exception as e:
        message = "Populate failed:  " + str(e)
    return JsonResponse({"message": message})


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
        
        return HttpResponse("Test users successfully created.")
    except Exception as e:
        return HttpResponse(f"Failed to create test users: {str(e)}", status=500)
