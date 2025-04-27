import firebase_admin
from firebase_admin import credentials, firestore

# 1. Connect to Firebase
cred = credentials.Certificate('C:/Angela/school/college/first year/2nd-sem/oop/database/database-table-badc5-firebase-adminsdk-fbsvc-fee7cfa592.json')  # <-- your JSON file here
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Initialize Firestore (or use Realtime Database if needed)
db = firestore.client()  # Firestore
# db = firebase_admin.db  # Uncomment if you're using Realtime Database

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from firebase_admin import firestore
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from django.contrib.auth.tokens import default_token_generator

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            # Add user to Firestore
            from database.firestore_connect import db
            user_data = {
                'email': user.email,
                'username': user.username,
                'date_joined': firestore.SERVER_TIMESTAMP
            }
            db.collection('users').document(str(user.id)).set(user_data)

            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('user/email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            email = EmailMessage(
                mail_subject, message, to=[form.cleaned_data.get('email')]
            )
            email.send()
            
            messages.success(request, 'Please confirm your email address to complete the registration')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Thank you for your email confirmation. You can now login to your account.')
        sync_user_to_firestore(user)
        return redirect('home')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('home')

def sync_user_to_firestore(user):
    """
    Creates or updates a Firestore document under `users/{user.pk}` 
    with email, username, is_active, and date_joined.
    """
    doc_ref = db.collection("users").document(str(user.pk))
    doc_ref.set({
        "email":       user.email,
        "username":    user.username,
        "is_active":   user.is_active,
        "date_joined": user.date_joined.isoformat()
    })

@login_required
def home(request):
    return render(request, 'user/index.html')
