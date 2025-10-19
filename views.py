from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .froms import SignUpForm, UpdateRegionForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        template_data['form'] = SignUpForm()
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = SignUpForm(request.POST, error_class=CustomErrorList)
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('accounts.login')
        
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'

    if request.method == 'GET':
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})
        
@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
        {'template_data': template_data})


@login_required
def update_region(request):
    profile = request.user.profile

    if request.method == "POST":
        form = UpdateRegionForm(request.POST, instance = profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Region updated successfully.')
            return redirect('trending.map')
    else:
        form = UpdateRegionForm(instance = profile)

    template_data = {
        'title' : 'Update Region',
        'form' : form
    }

    return render(request,'accounts/update_region.html', {'template_data': template_data})
