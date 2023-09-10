from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login
# Create your views here.
def sign_up(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            # Check if any field is missing
            if not username or not email or not password or not confirm_password:
                return render(request, 'signup.html', {'message': 'Please fill all the fields.'})

            # Check if username or email already exists
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                return render(request, 'signup.html', {'message': 'Username or email already exists.'})

            # Check if password and confirm_password match
            if password != confirm_password:
                return render(request, 'signup.html', {'message': 'Passwords do not match.'})

            # Additional password restrictions
            if len(password) < 8:
                return render(request, 'signup.html', {'message': 'Password should be at least 8 characters long.'})

            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            return render(request, 'signup.html', {'message': 'You have successfully signed up. Please login now.'})

        return render(request, 'signup.html')
    else:
        return redirect('/')
    
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Check if any field is missing
        if not username or not password:
            return render(request, 'login.html', {'message': 'Please fill all the fields.'})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Replace 'home' with the name of your home page URL
        else:
            return render(request, 'login.html', {'message': 'Username or password is incorrect'})

    return render(request, 'login.html')