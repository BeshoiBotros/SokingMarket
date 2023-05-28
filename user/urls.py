from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('customer/register/', views.CustomerRegistration.as_view(), name='customer_registration'),
    path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('customer/add-to-cart/<int:item>/', views.addToCart, name='add_to_cart'),
    path('customer/create-order/<int:item>/', views.createOrder, name='create_order'),
    path('customer/view-products/', views.ViewItems.as_view(), name='view_items'),
    path('customer/view-product/<int:pk>/', views.RetrieveItem.as_view(), name='view_item'),
    path('customer/profile/', views.RetrieveProfile.as_view(), name='retrieve_profile'), 
    path('customer/personal-info/', views.RetrievePersonalData.as_view(), name='personal_info'),
    path('customer/reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('customer/reset-password/confirm/<int:user_id>/<str:token>/', views.ConfirmPasswordReset.as_view(), name='confirm_password_reset'),
    
]

