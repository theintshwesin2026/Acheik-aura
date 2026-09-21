from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Product, Category, SubCategory, SubSubCategory, Order, CustomUser
from .forms import RegisterForm, LoginForm, ProfilePictureForm, UserProfileForm
from django.db.models import Q

def get_categories_context():
    """Helper function to get categories for all pages"""
    return {
        'categories': Category.objects.prefetch_related(
            'subcategories__subsubcategories'
        ).all()
    }

def ensure_categories_exist():
    """Ensure all categories, subcategories, and subsubcategories exist"""
    try:
        # Wedding Collection
        wedding, created = Category.objects.get_or_create(
            name="Wedding Collection",
            slug="wedding-collection"
        )
        
        # Special Ceremonial Wear
        special, created = Category.objects.get_or_create(
            name="Special Ceremonial Wear",
            slug="special-ceremonial-wear"
        )
        
        # Silk & Fabric
        silk, created = Category.objects.get_or_create(
            name="Silk & Fabric",
            slug="silk-fabric"
        )
        
        # Wedding Collection Subcategories
        women_wedding, created = SubCategory.objects.get_or_create(
            category=wedding,
            name="Women",
            slug="women-wedding"  # Changed slug to be unique
        )
        
        men_wedding, created = SubCategory.objects.get_or_create(
            category=wedding,
            name="Men", 
            slug="men-wedding"  # Changed slug to be unique
        )
        
        couple, created = SubCategory.objects.get_or_create(
            category=wedding,
            name="Couple",
            slug="couple"
        )
        
        # Special Ceremonial Wear Subcategories
        women_special, created = SubCategory.objects.get_or_create(
            category=special,
            name="Women",
            slug="women-special"
        )
        
        men_special, created = SubCategory.objects.get_or_create(
            category=special,
            name="Men",
            slug="men-special"
        )
        
        # Silk & Fabric Subcategories
        silk_textiles, created = SubCategory.objects.get_or_create(
            category=silk,
            name="Silk Textiles",
            slug="silk-textiles"
        )
        
        cotton_textiles, created = SubCategory.objects.get_or_create(
            category=silk,
            name="Cotton Textiles", 
            slug="cotton-textiles"
        )
        
        mixed_fibers, created = SubCategory.objects.get_or_create(
            category=silk,
            name="Mixed Fibers",
            slug="mixed-fibers"
        )
        
        # Wedding Collection Subsubcategories
        bridal_sets, created = SubSubCategory.objects.get_or_create(
            subcategory=women_wedding,
            name="Bridal Sets",
            slug="bridal-sets"
        )
        
        bridal_longyis, created = SubSubCategory.objects.get_or_create(
            subcategory=women_wedding,
            name="Bridal Longyis",
            slug="bridal-longyis"
        )
        
        # Special Ceremonial Wear Subsubcategories
        acheik_aura, created = SubSubCategory.objects.get_or_create(
            subcategory=women_special,
            name="Acheik Aura Limited Collection",
            slug="acheik-aura-limited"
        )
        
        blended_acheik, created = SubSubCategory.objects.get_or_create(
            subcategory=women_special,
            name="Blended Acheik & Longyis",
            slug="blended-acheik-longyis"
        )
        
        premium_acheik, created = SubSubCategory.objects.get_or_create(
            subcategory=women_special,
            name="Premium Acheik Collection", 
            slug="premium-acheik"
        )
        
        longyis, created = SubSubCategory.objects.get_or_create(
            subcategory=men_special,
            name="Longyis",
            slug="longyis"
        )
        
        teikpone_combo, created = SubSubCategory.objects.get_or_create(
            subcategory=men_special,
            name="Teikpone & Longyi Combo",
            slug="teikpone-longyi-combo"
        )
        
    except Exception as e:
        print(f"Error creating categories: {e}")

# FIXED: Updated shop_subcategory view to handle duplicate slugs
def shop_subcategory(request, category_slug, subcategory_slug):
    """View for specific subcategory"""
    # Get the category first
    category = get_object_or_404(Category, slug=category_slug)
    
    # Use filter() instead of get() and check for the specific category
    try:
        subcategory = SubCategory.objects.get(
            category=category, 
            slug=subcategory_slug
        )
    except SubCategory.DoesNotExist:
        # Try to find by name if slug doesn't match exactly
        subcategory = SubCategory.objects.filter(
            category=category,
            slug__icontains=subcategory_slug
        ).first()
        
        if not subcategory:
            raise Http404("Subcategory not found")
    
    # Get products from this specific subcategory
    products = Product.objects.filter(subcategory=subcategory)
    
    # Handle search
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(subcategory__name__icontains=query)
        )
    
    context = get_categories_context()
    context.update({
        'category': category,
        'subcategory': subcategory,
        'products': products,
    })
    
    return render(request, 'shop.html', context)

# FIXED: Updated shop_subsubcategory view
def shop_subsubcategory(request, category_slug, subcategory_slug, subsubcategory_slug):
    """View for specific subsubcategory"""
    # Get the category and subcategory first
    category = get_object_or_404(Category, slug=category_slug)
    
    try:
        subcategory = SubCategory.objects.get(
            category=category, 
            slug=subcategory_slug
        )
    except SubCategory.DoesNotExist:
        # Try to find by name if slug doesn't match exactly
        subcategory = SubCategory.objects.filter(
            category=category,
            slug__icontains=subcategory_slug
        ).first()
        
        if not subcategory:
            raise Http404("Subcategory not found")
    
    # Get the subsubcategory
    subsubcategory = get_object_or_404(
        SubSubCategory, 
        subcategory=subcategory,
        slug=subsubcategory_slug
    )
    
    products = Product.objects.filter(subsubcategory=subsubcategory)
    
    context = get_categories_context()
    context.update({
        "products": products,
        "current_category": category,
        "current_subcategory": subcategory,
        "current_subsubcategory": subsubcategory,
    })
    
    return render(request, "shop.html", context)

# Update all your views to include categories context
def homepage(request):
    ensure_categories_exist()
    context = get_categories_context()
    return render(request, 'main/homepage.html', context)

def about(request):
    context = get_categories_context()
    return render(request, 'main/aboutus.html', context)

def knowledge(request):
    context = get_categories_context()
    return render(request, 'main/knowledge.html', context)

def skinanalysis(request):
    context = get_categories_context()
    return render(request, 'main/skinanalysis.html', context)

def shop(request):
    ensure_categories_exist()
    
    # Get filters from query params
    category_slug = request.GET.get("category")
    subcategory_slug = request.GET.get("subcategory")
    subsubcategory_slug = request.GET.get("subsubcategory")
    search_query = request.GET.get('q')
    skin_tone = request.GET.get("skintone")

    products = Product.objects.all()

    # Apply filters
    if subsubcategory_slug:
        products = products.filter(subsubcategory__slug=subsubcategory_slug)
    elif subcategory_slug:
        products = products.filter(subcategory__slug=subcategory_slug)
    elif category_slug:
        products = products.filter(category__slug=category_slug)
    

    # Apply search filter
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    # Apply skin tone filter
    if skin_tone:
        products = products.filter(skin_tone__iexact=skin_tone)

    context = get_categories_context()
    context.update({
        "products": products,
        "search_query": search_query,
        "skin_tone": skin_tone,
    })
    
    return render(request, "shop.html", context)

def shop_category(request, category_slug):
    """View for specific category"""
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    
    context = get_categories_context()
    context.update({
        "products": products,
        "current_category": category,
    })
    
    return render(request, "shop.html", context)

@login_required
def change_profile_picture(request):
    if request.method == "POST":
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfilePictureForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'main/edit_profile.html', {
        'form': form
    })

def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, "signup.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html')
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            try:
                user_obj = CustomUser.objects.get(email=username_or_email)
                username = user_obj.username
            except CustomUser.DoesNotExist:
                username = username_or_email

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("/profile")
            else:
                msg = 'Wrong Username or Password'
                form = LoginForm(request, data=request.POST)
                return render(request, 'login.html', {'form': form, 'msg': msg})

    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("home")

def descriptioncard(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = get_categories_context()
    context.update({'product': product})
    return render(request, 'main/descriptioncard.html', context)

def productdetail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = get_categories_context()
    context.update({'product': product})
    return render(request, 'main/productdetail.html', context)

def home(request): 
    context = get_categories_context()
    return render(request, 'home.html', context)

def profile(request): 
    context = get_categories_context()
    return render(request, 'main/profile.html', context)

def signout(request):
    logout(request)
    return redirect('/')

def designerpage(request):
    context = get_categories_context()
    return render(request, "Designerpage.html", context)

def designgallery(request):
    context = get_categories_context()
    return render(request, "Designgallery.html", context)

def designgallery2(request):
    context = get_categories_context()
    return render(request, "designgallery2.html", context)

def designgallery3(request):
    context = get_categories_context()
    return render(request, "designgallery3.html", context)

def filter_products(request):
    availability = request.GET.get("availability")
    color = request.GET.get("color")
    min_price = request.GET.get("minPrice")
    max_price = request.GET.get("maxPrice")
    skin_tone = request.GET.get("skintone")

    products = Product.objects.all()

    if availability:
        products = products.filter(availability=availability)
    if color:
        products = products.filter(color__iexact=color)
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)
    if skin_tone:
        products = products.filter(skin_tone__iexact=skin_tone)

    data = []
    for p in products:
        data.append({
            "name": p.name,
            "description": p.description,
            "price": f"MMK{p.price:,.2f}",
            "availability": p.availability,
            "color": p.color,
            "image": p.image.url,
            "hover_image": p.hover_image.url if p.hover_image else "",
        })

    return JsonResponse({"products": data})

def checkoutpage(request):
    """Render the checkout page"""
    context = get_categories_context()
    return render(request, 'checkoutpage.html', context)

def place_order(request):
    if request.method == "POST":
        email = request.POST.get('email')
        country = request.POST.get('country')
        username = request.POST.get('username')
        address = request.POST.get('customer_address')
        city = request.POST.get('customer_city')
        phone = request.POST.get('customer_phone')
        payment = request.POST.get('payment')
        shipping = request.POST.get('shipping')
        subtotal = request.POST.get('voucherSubtotal') or 0
        shipping_fee = request.POST.get('voucherShipping') or 0
        total = request.POST.get('voucherTotal') or 0

        order = Order.objects.create(
            email=email,
            country=country,
            username=username,
            customer_address=address,
            customer_city=city,
            customer_phone=phone,
            payment_method=payment,
            shipping_method=shipping,
            subtotal=subtotal,
            shipping_fee=shipping_fee,
            total=total
        )

        messages.success(request, "✅ Your order has been placed successfully!")
        return redirect('order_success')

    context = get_categories_context()
    return render(request, 'checkout.html', context)

def order_success(request):
    """Order success page"""
    context = get_categories_context()
    return render(request, 'order_success.html', context)