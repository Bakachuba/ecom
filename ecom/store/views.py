from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from store.forms import SignUpForm, UpdateUserForm
from store.models import Product, Category


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None,
                                   instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, 'User account has been updated')
            return redirect('home')
        return render(request, 'store/update_user.html',
                      {'user_form': user_form})

    else:
        messages.error(request, 'You must be logged in to access that page')
        return redirect('home')


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'store/category_summary.html',
                  {'categories': categories})


def category(request, foo):
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'store/category.html',
                      {'products': products, 'category': category})
    except:
        messages.error(request, 'That Category Does Not Exist')
        return redirect('home')


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'store/product.html',
                  {'product': product})


def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})


def about(request):
    return render(request, 'store/about.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        # in login.html name='username'
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You Have Been Logged In')
            return redirect('home')

        else:
            messages.error(request, 'There was an error, please try again')
            return redirect('login')

    else:
        return render(request, 'store/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have registered successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Whoops! There was a problem with your registery, please try again')
            return redirect('register')
    else:
        return render(request, 'store/register.html', {'form': form})
