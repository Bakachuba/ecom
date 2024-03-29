import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect

from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from store.forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from store.models import Product, Category, Profile


def search(request):
    # determine if they filled out the form

    if request.method == 'POST':
        searched = request.POST['searched']
        # query the products db model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        # test for null
        if not searched:
            messages.error(request, 'Product not found')
            return render(request, 'store/search.html', {})
        else:
            return render(request, 'store/search.html', {'searched': searched})
    else:
        return render(request, 'store/search.html', {})


def update_info(request):
    if request.user.is_authenticated:
        # Get current user
        current_user = Profile.objects.get(user__id=request.user.id)
        # Get current user's shipping info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        # Get original user form
        form = UserInfoForm(request.POST or None,
                            instance=current_user)

        # Get user's shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            # Save original form
            form.save()
            # Save shipping form
            shipping_form.save()

            messages.success(request, 'Your info has been updated')
            return redirect('home')
        return render(request, 'store/update_info.html',
                      {'form': form, 'shipping_form': shipping_form})

    else:
        messages.error(request, 'You must be logged in to access that page')
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been updated!')
                return redirect('update_user')

            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'store/update_password.html', {'form': form})

    else:
        messages.error(request, 'You must be logged in to access that page')
        return redirect('home')


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

            # do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            # get the saved cart from db
            saved_cart = current_user.old_cart
            # convert db str to python dictionary
            if saved_cart:
                # convert to dictionary using json
                converted_cart = json.loads(saved_cart)
                # add the loaded cart dictionary to our session
                # get the cart
                cart = Cart(request)
                # loop thru the cart and add the items from the db
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

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
            messages.success(request, 'Username Created - Please Fill out your user info below')
            return redirect('update_info')
        else:
            messages.error(request, 'Whoops! There was a problem with your registery, please try again')
            return redirect('register')
    else:
        return render(request, 'store/register.html', {'form': form})
