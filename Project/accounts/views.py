from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from accounts.forms import RegistrationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from accounts.models import User
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text
from accounts.tokens import account_activation_token
from django.contrib.auth import login,authenticate
from django.core.mail import EmailMessage
def Registration(request):
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            #============Emailing======
            current_site=get_current_site(request)
            mail_subject="Activate your blog account."
            message=render_to_string('activation_email.html',{
            'user':user,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
            })
            to_mail=form.cleaned_data.get('email')
            email=EmailMessage(
            mail_subject,message,to=[to_mail]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the Registration')

    else:
        form=RegistrationForm()
    context={
    'form':form
    }
    return render(request,'accounts/register.html',context)
def ActivateView(request,uidb64,token):
    try:
        uid=force_text(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except:
        user=None
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active=True
        user.save()
        login(request,user)
        return HttpResponse('Thank you for you email Confirmation.Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
