from rest_framework import serializers
from base.models.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id' , 'username']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Profile
        fields = ('user', 'first_name', 'last_name', 'email')



class ItemSerializer(serializers.ModelSerializer):
    seller = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Item
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    Item = ItemSerializer(read_only=True)
    buyer = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Transaction
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    item = ItemSerializer(read_only=True)
    class Meta:
        model = Cart
        fields = '__all__'

