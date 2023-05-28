from rest_framework import generics
from .serializers import CustomerRegistrationSerializer, ProfileSerializer, CartSerializer, OrderSerializer, ItemSerializer, Profile, PersonalDataSerializer, ResetPasswordSerializer, ConfirmationPasswordResetSrializer, ChangePasswordSerializer
from .models import Customer, Cart, Order, Item
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .pagination import ProductsPagination
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status
from django.contrib.auth.hashers import make_password

class CustomerRegistration(generics.CreateAPIView):
    serializer_class = CustomerRegistrationSerializer
    queryset = Customer.objects.all()


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

class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = Customer.objects.get(email=email)
            except Customer.DoesNotExist:
                return Response({'msg' : 'user Does not Exist'}, status=status.HTTP_400_BAD_REQUEST)
            
            token = default_token_generator.make_token(user)
            reset_password_url = f'http://127.0.0.1:8000/customer/reset-password/confirm/{user.id}/{token}/'

            send_mail(
                'Reset Your Password',
                f'Click the following link to reset your password: {reset_password_url} your mother F***** B****',
                'beshoibotros111@gmail.com',
                [email],
                fail_silently=False,
                
            )

            return Response({'msg' : 'we will send password reset link for you now'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfirmPasswordReset(APIView):
    def post(self, request, user_id, token):
        try:
            user = Customer.objects.get(id=user_id)
        except Customer.DoesNotExist:
            return Response({'msg' : 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        if default_token_generator.check_token(user, token):
            serializer = ConfirmationPasswordResetSrializer(data=request.data)
            if serializer.is_valid():
                password = serializer.validated_data['new_password']
                user.password = make_password(password)
                user.save()
                return Response({'msg' : 'the password has been reseted successfully'})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid reset token.'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            if not request.user.check_password(old_password):
                return Response({'msg' : 'inavlid password!'}, status=status.HTTP_400_BAD_REQUEST)
            request.user.password = make_password(new_password)
            request.user.save()
            return Response({'msg' : 'password changed successfuly'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)