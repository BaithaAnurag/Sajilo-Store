from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Profile
from .forms import ContactForm
from django.core.paginator import Paginator



##Product Homepage 
def home(request):
    featured_products = Product.objects.filter(is_featured=True)
    return render(request, 'home.html', {
        'featured_products': featured_products
    })


##About Us 
def About_view(request):
    return render(request, 'about.html')


#Feature Producted 
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        try:
            new_rating = int(request.POST.get('rating'))
            if 1 <= new_rating <= 5:
                # Update average
                total_rating = product.rating * product.rating_count
                product.rating_count += 1
                product.rating = (total_rating + new_rating) / product.rating_count
                product.save()
        except:
            pass 

    return render(request, 'featured_products_items.html', {'product': product})



#Rateing Products 
def rate_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        rating = int(request.POST.get('rating', 0))
        product.rating = rating
        product.save()
        return redirect('feature', product_id=product.id)

    return render(request, 'rate_product.html', {'product': product})    

#add to cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})
    cart[str(product.id)] = cart.get(str(product.id), 0) + 1
    request.session['cart'] = cart

    messages.success(request, f"{product.name} added to cart!")

    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('shop') 


#Remove From Cart
def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        if product_id_str in cart:
            if cart[product_id_str] > 1:
                cart[product_id_str] -= 1
                messages.success(request, f'Removed one quantity of the product.')
            else:
                del cart[product_id_str]
                messages.success(request, f'Removed the product from your cart.')
            request.session['cart'] = cart
        else:
            messages.warning(request, 'Product not found in your cart.')

    return redirect('view_cart') 



#coupen
def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('coupon_code')
        # Add your coupon logic here (e.g., validate, apply discount)
        # For now, just a placeholder
        print(f"Coupon applied: {code}")
    return redirect('view_cart')  # or wherever your cart view name is



@login_required
def shop(request):
    products = Product.objects.all()
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop.html', {'page_obj': page_obj})




#View of Cart

@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []

    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
    })
 



##Contact Us form
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'thank_you.html')  
    else:
        intial_data = {'name':'','email':'','message':''}
        form = ContactForm(initial=intial_data)
    return render(request, 'contact.html', {'form': form})


#Signup Views
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        gender = request.POST['gender']
        phone = request.POST['phone']
        city = request.POST['city']
        image = request.FILES.get('image')
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('signup_view')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('signup_view')

        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(
            user=user,
            phone=phone,
            gender=gender,
            city=city,
            image=image
        )
        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login_view')

    return render(request, 'signup.html')




#Login Views 
def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next') or 'shop'

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        remember = request.POST.get('remember_me')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if remember != 'on':
                request.session.set_expiry(0)  # expire on browser close
            else:
                request.session.set_expiry(1209600)  # 2 weeks

            return redirect(next_url)

        messages.error(request, "Invalid username or password.")

    return render(request, 'login.html', {'next': next_url})


#Resert Passord 

def reset_password_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not new_password or not confirm_password:
            messages.error(request, "All fields are required.")
        elif new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            try:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password reset successfully. You can now log in.")
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, "User does not exist.")

    return render(request, 'reset_password.html')


#Logout Views
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')



##User Profile 
@login_required
def profile_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        # Option 1: create profile if it doesn't exist
        profile = Profile.objects.create(user=request.user)
        # Option 2: redirect to a profile creation form
        # return redirect('profile_create')
    return render(request, 'user_profile.html', {'profile': profile})


#Profile Edit MOdel
@login_required
def profile_edit(request):
    profile = request.user.profile
    
    if request.method == 'POST':
        profile.phone = request.POST.get('phone')
        profile.city = request.POST.get('city')
        profile.gender = request.POST.get('gender')
        profile.region_state = request.POST.get('region_state')
        district = request.POST.get('district')
        if not district:
            messages.error(request, "District is required.")
            return render(request, 'profile_edit.html', {'profile': profile})
        profile.district = district

        age = request.POST.get('age')
        profile.age = int(age) if age and age.isdigit() else None

        if 'image' in request.FILES:
            profile.image = request.FILES['image']

        profile.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profile_view')  # Make sure your URL name matches

    return render(request, 'profile_edit.html', {'profile': profile})




#men Fashion 
def men_fashion_view(request):
    products = Product.objects.filter(category='men')
    return render(request, 'men_fashion.html', {'Products': products})


def type_view(request):
    types = Product.objects.filter( type='T-Shirt', category='men')
    return render(request, 'type.html', {'types': types})

def shirt_view(request):
    shirt = Product.objects.filter( type='Shirt', category='men')
    return render(request, 'shirt.html', {'shirt': shirt})

def jeans_view(request):
    jeanss = Product.objects.filter( type='jeans', category='men')
    return render(request, 'jeans.html', {'jeanss': jeanss})   

def shoes_view(request):
    shoeses = Product.objects.filter( type='shoes', category='men')
    return render(request, 'shoes.html', {'shoeses': shoeses})  

def accessories_view(request):
    accessorieses = Product.objects.filter( type='accessories', category='men')
    return render(request, 'accessories.html', {'accessorieses': accessorieses})  

#Women Fashion 


def women_type_view(request):
    types = Product.objects.filter( category='women')
    return render(request, 'Women_Fashion/type.html', {'types': types})


def accessories_view(request):
    accessorieses = Product.objects.filter(type='accessories', category='women')
    return render(request, 'Women_Fashion/accessories.html', {'accessorieses': accessorieses})  



#Payment 


def payment_view(request):
    return render(request, 'payment/payment.html')
