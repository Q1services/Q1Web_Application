from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm 
from .models import Account
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string 
from Q1Project import settings

# routes to index.html
def home(request):
    return render(request, 'users/index.html')

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            month = request.POST['dob_month']
            day = request.POST['dob_day']
            year = request.POST['dob_year']
            obj.dob = f'{year}-{month}-{day}'
            obj.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = Account.objects.get(email=email)
            user.hash_val = user.id
            user.save()
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('verification', hash_val=user.hash_val.hashid)

        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'users/register.html', context) 


# sends html mail to a new user
def email_verification(request, hash_val):
        html_template = render_to_string('users/templatemail.html', {'hash_val' : hash_val, 'env':settings.DEBUG})
        to_email = Account.objects.get(hash_val=hash_val).email
        send_mail('Verification Email from Q1services', None, 'q1services123@gmail.com', [to_email], html_message=html_template, fail_silently=False)
        messages.info(request, f'Mail has been sent to your email. Click on Verify for the verification of your email.')
        return redirect('register')

# verifies mail and confirm to the database
def email_verified(request, hash_val):
    user = Account.objects.get(hash_val=hash_val)
    user.email_verified = True
    user.save()
    messages.success(request, 'Congratulations! Your email has been verified. You can now login')
    return render(request, 'users/index.html')