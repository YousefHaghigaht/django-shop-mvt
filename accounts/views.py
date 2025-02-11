from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegisterForm,VerifyCodeForm,UserLoginForm
from utils import send_otp_code
import random
from django.contrib import messages
from .models import OtpCode,User
from datetime import datetime,timedelta
import pytz
from django.contrib.auth import authenticate,login,logout


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_class = 'accounts/register.html'

    def get(self,request):
        form = self.form_class
        return render(request,self.template_class,{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            request.session['user_registration_info'] = {
                'phone_number':cd['phone_number'],
                'email':cd['email'],
                'full_name':cd['full_name'],
                'password':cd['password1']
            }
            random_code = random.randint(10000,99999)
            OtpCode.objects.create(phone_number=cd['phone_number'], code=random_code)
            send_otp_code(cd['phone_number'],random_code)
            messages.success(request,'We sent a code on your phone number','success')
            return redirect('accounts:verify_code')


class VerifyCodeView(View):
    form_class = VerifyCodeForm
    template_class = 'accounts/verify_code.html'
    expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=1)

    def setup(self,request,*args,**kwargs):
        self.user_session = request.session['user_registration_info']
        self.code_instance = OtpCode.objects.get(phone_number=self.user_session['phone_number'])
        return super().setup(request,*args,**kwargs)

    def get(self,request):
        form = self.form_class
        disable_btn = False
        if self.code_instance.created < self.expired_time:
            disable_btn = True
        return render(request,self.template_class,{'form':form,'disable_btn':disable_btn})

    def post(self,request):
        form = self.form_class(request.POST)
        user_session = self.user_session
        code_instance = self.code_instance
        if form.is_valid():
            if code_instance.code == form.cleaned_data['code'] and code_instance.created > self.expired_time:
                User.objects.create_user(
                    phone_number=user_session['phone_number'],
                    email=user_session['email'],
                    full_name=user_session['full_name'],
                    password=user_session['password']
                )
                code_instance.delete()
                messages.success(request,'You have successfully registered','success')
                return redirect('home:home')
            elif code_instance.created < self.expired_time :
                messages.error(request,'The entered code expired','danger')
                return redirect('accounts:verify_code')
            else:
                messages.error(request,'The entered code is not correct','danger')
                return redirect('accounts:verify_code')

class ResendCodeView(View):

    def setup(self,request,*args,**kwargs):
        self.user_session = request.session['user_registration_info']
        self.code_instance = OtpCode.objects.get(phone_number=self.user_session['phone_number'])
        return super().setup(request,*args,**kwargs)

    def dispatch(self, request, *args, **kwargs):
        expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=1)
        if self.code_instance.created > expired_time:
            messages.error(request,'Your code has not yet expired','danger')
            return redirect('accounts:verify_code')
        else:
            OtpCode.objects.filter(phone_number=self.user_session['phone_number']).delete()
            return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        random_code = random.randint(10000,99999)
        OtpCode.objects.create(phone_number=self.user_session['phone_number'],code=random_code)
        messages.success(request,'We resent code on your phone number ','success')
        return redirect('accounts:verify_code')

class UserLoginView(View):
    form_class = UserLoginForm
    template_class = 'accounts/login.html'

    def get(self,request):
        form = self.form_class
        return render(request,self.template_class,{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['phone_number'],password=cd['password'])
            if user:
                login(request,user)
                messages.success(request,'You have successfully logged in',('success'))
                return redirect('home:home')
            else:
                messages.error(request,'The phone number does not match the password','danger')
                return redirect('accounts:login')


class UserLogoutView(View):

    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,'You are not logged into your account.','danger')
            return redirect('home:home')
        else:
            return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        logout(request)
        messages.success(request,'You have successfully logged out','success')
        return redirect('home:home')







