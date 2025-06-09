from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

        path('', views.home, name='home'),

        path('signup/', views.signup_view, name='signup_view'),
        path('login/', views.login_view, name='login_view'),
        path('logout/', views.logout_view, name='logout_view'),
        path('about/', views.About_view, name='About_view'),
        path('reset-password/', views.reset_password_view, name='reset_password_view'),
        path('contact/', views.contact_view, name='contact_view'),
        path('contact/', views.contact_view, name='contact_view'),
        path('feature/<int:pk>/', views.product_detail, name='product_detail'),
        path('product/<int:product_id>/rate/', views.rate_product, name='rate_product'),
        path('cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
        path('shop/', views.shop, name='shop'),
        path('cart/', views.cart_view, name='view_cart'),
        path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
        path('apply-coupon/', views.apply_coupon, name='apply_coupon'),

        
        #MEN pRODUCTS
        path('fashion_men/', views.men_fashion_view, name='men_fashion_view'),
        path('view_type/', views.type_view, name='type_view'),
        path('view_shirt/', views.shirt_view, name='shirt_view'),
        path('view_jeans/', views.jeans_view, name='jeans_view'),
        path('view_shoes/', views.shoes_view, name='shoes_view'),
        path('view_accessories/', views.accessories_view, name='accessories_view'),

        #wOMEN PRODUCTS 
        path('women_type/', views.women_type_view, name='women_type_view'),

        path('profile/',views. profile_view, name='profile_view'),
        path('profile/edit/', views.profile_edit, name='profile_edit'),


           # eSewa
       
        path('view_payment', views.payment_view, name='payment_view'),

     

                                


] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
                 