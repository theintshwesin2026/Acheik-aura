from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('change-profile-picture/', views.change_profile_picture, name='change_profile_picture'),
    path('aboutus/', views.about, name='about'),
    path('knowledge/', views.knowledge, name='knowledge'),
    path('skinanalysis/', views.skinanalysis, name='skinanalysis'),
    path("logout/", views.logout_view, name="logout"),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('home/', views.home, name='home'),
    path('product/<int:product_id>/', views.descriptioncard, name='descriptioncard'),
    path('designerpage/', views.designerpage, name='designerpage'),
    path('designgallery/', views.designgallery, name='designgallery'),
    path('designgallery2/', views.designgallery2, name='designgallery2'),
 path('designgallery3/', views.designgallery3, name='designgallery3'),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    
    # Shop URLs
    path('shop/', views.shop, name='shop'),
    path('shop/category/<slug:category_slug>/', views.shop_category, name='shop_category'),
    path('shop/category/<slug:category_slug>/<slug:subcategory_slug>/', views.shop_subcategory, name='shop_subcategory'),
    path('shop/category/<slug:category_slug>/<slug:subcategory_slug>/<slug:subsubcategory_slug>/', views.shop_subsubcategory, name='shop_subsubcategory'),
    path("filter/", views.filter_products, name="filter_products"),
    
    path('checkout/', views.checkoutpage, name='checkoutpage'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)