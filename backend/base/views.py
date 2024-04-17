from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.models import User
from base.models import Item , Cart , Transaction
from base.forms import ItemPriceEditForm , ItemForm
from django.http import HttpResponse , JsonResponse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin , LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.utils.translation import ugettext as _


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
        Item.objects.all().delete()
        # Generate new test users
        z = 1
        for i in range(1, 7):
            username =  f'testuser{i}'
            email = f'{username}@shop.aa'
            password = f'pass{i}'
            user = User.objects.create_user(username=username, email=email, password=password)
            
            if i <= 3 :
                 for j in range(1, 11):
                    title = f'title{z}'
                    description = f'description{z}'
                    price = random.randint(MIN_ITEM_PRICE , MAX_ITEM_PRICE )
                    date_added = datetime.datetime.now()
                    item = Item.objects.create(title=title , description=description , price=price , seller=user , date_added = date_added)
                    z+=1
                 
                 
        
        return HttpResponse("Test users successfully created.")
    except Exception as e:
        return HttpResponse(f"Failed to create test users: {str(e)}", status=500)


class ItemDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Item



class ItemListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Item
    paginate_by = 20
    
    def get_queryset(self):
        
        return Item.objects.all().filter(is_sold=False).order_by('id')





class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html" 




class ItemCreate(generic.edit.CreateView , LoginRequiredMixin):
    model = Item
    fields = ['description', 'image', 'price', 'seller' , 'date_added']
    initial = {'date_of_death': '11/11/2023'}
    #permission_required = 'base.add_ item'




class ItemSearchListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Item
    paginate_by = 10
    
    def get_queryset(self):

        search = self.request.GET.get('search' , None) # defaulting to None  may cause dome problem who knows using an empty string may cause problems 

                
        return Item.objects.all().filter(title__icontains = search ).filter (is_sold=False)
    
    

   

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was successfully updated!'))
            return redirect('password_reset_complete')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'base/change_password.html', {
        'form': form
    })
    


@login_required
def user_items(request):
    user = request.user
    on_sale_items = Item.objects.filter(seller=user, is_sold=False)
    sold_items = Item.objects.filter(seller=user, is_sold=True)
    purchased_items = Item.objects.filter(transaction__buyer=user)

    context = {
        'on_sale_items': on_sale_items,
        'sold_items': sold_items,
        'purchased_items': purchased_items,
    }
    return render(request, 'base/user_items.html', context)

@login_required
def edit_item_price(request, title):
    
    item = get_object_or_404(Item, title=title, seller=request.user, is_sold=False)
    #item = get_object_or_404(Item, title=title,  is_sold=False)
    
    if request.method == 'POST':
        form = ItemPriceEditForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            
            return redirect(item)  # Redirect to the user's items page after successful edit
    else:
        form = ItemPriceEditForm(instance=item)
        print ("items is ", item)
    return render(request, 'base/edit_item_price.html', {'form': form, 'item': item})


@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.date_added = datetime.datetime.now()
            item.save()
            return redirect(item)  # Redirect to the user's items page after adding the item
    else:
        form = ItemForm()
    
    return render(request, 'base/add_item.html', {'form': form})



@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    
    # Check if the user is trying to add their own item to the cart
    if request.user == item.seller:
        return redirect('item-detail', item_id=item_id)  # Redirect back to the item detail page
    
    # Check if the item is already in the user's cart
    if Cart.objects.filter(user=request.user, item=item).exists():
        # You can handle this case based on your application's requirements
        # For example, you might want to display a message to the user that the item is already in their cart
        return redirect('item-detail', item_id=item_id)
    
    # Add the item to the user's cart
    Cart.objects.create(user=request.user, item=item)
    
    return redirect('cart')  # Redirect to the user's cart page


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, pk=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).filter(item__is_sold=False)
    total_price = sum(cart_item.item.price * cart_item.quantity for cart_item in cart_items)
    
    if request.method == 'POST':
        for cart_item in cart_items:
            item = cart_item.item
            if item.price != cart_item.item.price:
                # Notify the user if the price of an item has changed
                messages.warning(request, f"The price of '{item.title}' has changed. Please review before proceeding.")
                return redirect('checkout')
            if item.is_sold:
                # Notify the user if an item is no longer available
                messages.warning(request, f"The item '{item.title}' is no longer available.")
                return redirect('checkout')
        
        # If all items are still available and their prices haven't changed, mark them as sold
        for cart_item in cart_items:
            cart_item.item.is_sold = True
            cart_item.item.save()
            transaction = Transaction.objects.create(buyer=request.user, item=item)  # Create a transaction for each item
            transaction.save()
            cart_item.delete()
        
        messages.success(request, "Transaction successful. Items have been marked as sold.")
        return redirect('my_items')
    
    return render(request, 'base/checkout.html', {'cart_items': cart_items, 'total_price': total_price})


    
@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'base/cart.html', {'cart_items': cart_items})


@login_required
def view_my_items(request):
    my_items = Item.objects.filter(seller=request.user)
    return render(request, 'base/my_items.html', {'my_items': my_items})


