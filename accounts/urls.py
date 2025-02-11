from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/',views.UserRegisterView.as_view(),name='register'),
    path('verify_code/',views.VerifyCodeView.as_view(),name='verify_code'),
    path('resend_code/',views.ResendCodeView.as_view(),name='resend_code'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout/',views.UserLogoutView.as_view(),name='logout')
]