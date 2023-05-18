from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth import login
from user.forms import UserRegistrationForm, LoginForm
from user.models import Profile
from user.forms import ProfileForm


def login_page(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.data.get('username'), password=form.data.get('password'))
            login(request, user)
            if user is not None:
                try:
                    profile = Profile.objects.get(owner_id=user.id)
                except:
                    profile = Profile(owner_id=user.id)
                    profile.save()
                return redirect('/')
            else:
                form.add_error(field='username', error='Invalid password or login')
                return render(request, 'user/login.html', {'form': form})
        else:
            return render(request, 'user/login.html', {'form': form})


def register_page(request):
    if request.method == 'GET':
        form = UserRegistrationForm()
        return render(request, 'user/register.html', {'form': form})
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            profile = Profile(owner_id=user.id)
            profile.save()
            auth_data = auth.authenticate(request, email=user.email, password=form.data.get('password'))
            if auth_data is not None:
                login(request, auth_data)
                return redirect('/')
            return redirect('/auth/login/')
        else:
            return render(request, 'user/register.html', {'form': form})


def logout_page(request):
    auth.logout(request)
    return redirect('/auth/login')


def settings_page(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(owner_id=request.user.id)

        if request.method == 'GET':
            form = ProfileForm(data={'bio': profile.bio}, files={'image': profile.image})
            return render(request, 'user/profile.html', {'form': form, 'profile': profile})
        if request.method == 'POST':
            form = ProfileForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                profile.image = form.files.get('image')
                profile.resume = form.files.get('resume')
                profile.bio = form.data.get('bio')
                profile.save()
                return render(request, 'user/profile.html', {'form': form, 'profile': profile})
            else:
                print(form.errors)
                return render(request, 'user/profile.html', {'form': form, 'profile': profile})
        return redirect('/')
    else:
        return redirect('/')
