from rest_framework import generics
from .serializers import CustomerRegistrationSerializer, ProfileSerializer, CartSerializer, OrderSerializer, ItemSerializer, Profile, PersonalDataSerializer
from .models import Customer, Cart, Order, Item
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .pagination import ProductsPagination

class CustomerRegistration(generics.CreateAPIView):
    serializer_class = CustomerRegistrationSerializer
    queryset = Customer.objects.all()

    def perform_create(self, serializer):
        customer = serializer.save()
        profile_data = {'user' : customer.id}
        profile_serializer = ProfileSerializer(data=profile_data)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()
        return customer

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addToCart(request, item):
    if request.method == 'POST':
        try:
            Cart.objects.get(id = item)
        except Cart.DoesNotExist:
            return Response({'msg' : 'item does not found'})
        cart_data = {'user' : request.user, 'item': item}
        cart_serializer = CartSerializer(data=cart_data)
        cart_serializer.is_valid(raise_exception=True)
        cart_serializer.save()
        return Response({'msg' : 'Item Added Successfully to your Cart'})

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])    
def createOrder(request, item):
    if request.method == 'POST':
        try:
            Order.objects.get(id = item)
        except Order.DoesNotExist:
            return Response({'msg' : 'item does not found'})
        quantity = request.POST.get('quantity')
        if quantity <= 0:
            return Response({'msg' : 'Quantity must greater then zero(0)'})
        order_data = {'user' : request.user, 'item': item, 'quantity' : quantity}
        cart_serializer = OrderSerializer(data=order_data)
        cart_serializer.is_valid(raise_exception=True)
        cart_serializer.save()
        return Response({'msg' : 'Item Added Successfully to your Cart'})

class ViewItems(generics.ListAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ProductsPagination
    queryset = Item.objects.all()

class RetrieveItem(generics.RetrieveAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = Item.objects.all()
    lookup_field = 'pk'

class RetrieveProfile(generics.RetrieveUpdateAPIView):

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        profile = Profile.objects.get(user = self.request.user)
        return profile

class RetrievePersonalData(generics.RetrieveUpdateAPIView):
    serializer_class = PersonalDataSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
