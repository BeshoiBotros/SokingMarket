from rest_framework import serializers
from .models import Customer, Profile, Cart, Order, Item
from django.contrib.auth.hashers import make_password
import re
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

def valid_phone_number(str):
    pattern = r'^20\d{8}$'
    if re.match(pattern, str):
        return True
    else:
        return False

def username_already_exist(username):
    return Customer.objects.filter(username = username).exists()

def phone_number_alredy_exist(ph):
    return Customer.objects.filter(phone_number = ph).exists()

class CustomerRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email    = serializers.CharField()
    password = serializers.CharField(write_only = True, style={'input_type': 'password'})
    password_confermation = serializers.CharField(write_only = True, style={'input_type': 'password'})
    address  = serializers.CharField()
    phone_number = serializers.CharField()

    def validate(self, attrs):
        password = attrs.get('password')
        password_confermation = attrs.get('password_confermation')
        username = attrs.get('username')
        email = attrs.get('email')
        phone_number = attrs.get('phone_number')
        if password != password_confermation:
            raise serializers.ValidationError('password does not matching with password confermation')
        if username == email:
            raise serializers.ValidationError('username and email can not be the same')
        if not email:
            raise serializers.Serializer('email must be set')
        if not username:
            raise serializers.ValidationError('username must be set')
        if not password:
            raise serializers.ValidationError('password must be set')
        if valid_phone_number(phone_number):
            raise serializers.ValidationError('phone number is invalid try another number')
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError(f'{e}')
        if username_already_exist(username):
            raise serializers.ValidationError('username already exist')
        if phone_number_alredy_exist(ph=phone_number):
            raise serializers.ValidationError('phone number alredy exist ')
        return attrs
        

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        email    = validated_data.get('email')
        address  = validated_data.get('address')
        phone_number = validated_data.get('phone_number')
        user = Customer(
            username = username,
            password = make_password(password),
            email = email,
            address = address,
            phone_number = phone_number
        )
        user.save()
        return user
    

class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_null = True, required=False)
    class Meta:
        model = Profile
        fields = ['user', 'image']
        read_only_fields = ['user']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if value is not None:
                setattr(instance, attr, value)
        instance.save()
        return instance

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__al__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class PersonalDataSerializer(serializers.Serializer):
    first_name   = serializers.CharField(allow_null = True, required=False)
    last_name    = serializers.CharField(allow_null = True, required=False)
    email        = serializers.EmailField(allow_null = True, required=False)
    address      = serializers.CharField(allow_null = True, required=False)
    phone_number = serializers.CharField(allow_null = True, required=False)
    
    class Meta:
        model  = Customer
        fields = ['first_name', 'last_name', 'email', 'address', 'phone_number']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if value is not None and attr != 'user':
                setattr(instance, attr, value)
        instance.save()
        return instance
    
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ConfirmationPasswordResetSrializer(serializers.Serializer):
    new_password = serializers.CharField(write_only = True, style={'input_type': 'password'})
    confirm_new_password = serializers.CharField(write_only = True, style={'input_type': 'password'})

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError('password does not match with confirmation password')
        return attrs
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.Serializer(write_only = True, style={'input_type': 'password'})
    new_password = serializers.Serializer(write_only = True, style={'input_type': 'password'})
    confirm_new_password = serializers.Serializer(write_only = True, style={'input_type': 'password'})

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError('new password does not match with new password confirmation')
        return