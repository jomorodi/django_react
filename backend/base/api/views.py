from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from base.models.models import Profile
from django.views.decorators.csrf import csrf_exempt
from base.models.models import Item , Transaction , Cart
import json

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from base.serializers.serializer import ProfileSerializer ,ItemSerializer , TransactionSerializer , CartSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    profile = user.profile
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)



@api_view(['GET'])
def get_routes(request):
   routes = [
       '/api/token',
       '/api/token/refresh',
       'api/token/verify/'
   ]
   return Response(routes)


@csrf_exempt
@api_view(('POST',))
def createUser(request):
    
    
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.data['username'],
            password=request.data['password'],
            email=request.data['email']
        )
        
        user.save()
        user.profile.first_name = request.data['first_name']  
        user.profile.last_name = request.data['last_name']
        user.profile.email = request.data['email']
        user.profile.save()    
        return Response(status=status.HTTP_200_OK)

 
@csrf_exempt
@api_view(('POST',))
def change_password(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.get_username())
        user.set_password(request.data['newPassword'])
        print (request.data['newPassword'] ,  'new password')
        user.save()
        return Response(status=status.HTTP_200_OK)
    



@api_view(('GET',))
def get_user_items(request):
    user = request.user
    items = user.profile.items.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)




@api_view(['GET'])
def items_for_sale(request):
    # Query all items for sale
    items = Item.objects.filter(is_sold=False)
    
    # Serialize the queryset using ItemSerializer
    serializer = ItemSerializer(items, many=True)
    
    # Return serialized data as JSON response
    return Response(serializer.data)


@api_view(['GET'])
def search_items(request):
    query = request.GET.get('query', '')
    if query:
        items = Item.objects.filter(title__icontains=query, is_sold=False)
        serialized_items = ItemSerializer(items, many=True).data
        return Response(serialized_items)
    else:
        return Response([])
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_item(request):
    serializer = ItemSerializer(data=request.data ,partial=True)
    if serializer.is_valid():
        serializer.save(seller=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def items_on_sale(request):
    items = Item.objects.filter(seller=request.user, is_sold=False)
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sold_items(request):
    items = Item.objects.filter(seller=request.user, is_sold=True)
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def purchased_items(request):
    transactions = Transaction.objects.filter(buyer=request.user)
    purchased_items = [transaction.item for transaction in transactions]
    serializer = ItemSerializer(purchased_items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    item_id = request.data.get('item_id')
    item = Item.objects.get(id=item_id)
    
    # Check if the item belongs to the current user
    if item.seller == request.user:
        return Response({"error": "You cannot add your own item to the cart."}, status=400)
    
    # Add the item to the cart
    cart_item = Cart.objects.create(user=request.user, item=item , price=item.price)
    return Response({"message": "Item added to cart successfully."}, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    cart_item_id = request.data.get('cart_item_id')
    try:
        cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
        cart_item.delete()
        return Response({"message": "Item removed from cart successfully."}, status=204)
    except Cart.DoesNotExist:
        return Response({"error": "Cart item not found."}, status=404)
    



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def items_to_purchase(request):
    cart_items = Cart.objects.filter(user=request.user)
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pay_for_items(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    # Check for price changes or item availability
    for cart_item in cart_items:
        item = cart_item.item
        if item.price != cart_item.price:
            return Response({"error": f"Price of item '{item.title}' has changed. Please update the price and try again."}, status=400)
        if item.is_sold:
            return Response({"error": f"Item '{item.title}' is no longer available."}, status=400)
    
    # Proceed with payment
    for cart_item in cart_items:
        item = cart_item.item
        item.is_sold = True
        item.save()
        Transaction.objects.create(item=item, buyer=request.user)
        cart_item.delete()
    
    return Response({"message": "Payment successful."}, status=200)




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_item_price(request):
    item_id = request.data.get('item_id')
    new_price = request.data.get('new_price')
    
    try:
        item = Item.objects.get(id=item_id, seller=request.user, is_sold=False)
        item.price = new_price
        item.save()
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    except Item.DoesNotExist:
        return Response({"error": "Item not found or cannot be edited."}, status=404)
    



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def item_details(request):
    item_id = request.query_params.get('item_id')
    try:
        item = Item.objects.get(id=item_id)
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    except Item.DoesNotExist:
        return Response({"error": "Item not found."}, status=404)