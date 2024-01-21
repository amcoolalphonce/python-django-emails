
from django.http import HttpResponse  
from django.shortcuts import render, redirect  
from django.contrib.auth import login, authenticate  
from .forms import SignupForm  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  

def signup(request):
   if request.method == 'POST':  
      form = SignupForm(request.POST)  
      if form.is_valid():  
         user = form.save(commit=False)   #save it memory and not database
         user.is_active = False  
         user.save()
         current_site = get_current_site(request)
         mail_subject =  'Activation link has been sent to your email id'  
         message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
          to_email = form.cleaned_data.get('email')  
         email = EmailMessage(  
                         mail_subject, message, to=[to_email]  )  
         email.send()
         return HttpResponse('Please confirm your email address to complete the registration')  
