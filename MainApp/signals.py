from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import CartItem

@receiver(user_logged_in)
def restore_cart(sender, request, user, **kwargs):
    session_cart = request.session.get('cart', {})
    db_cart_items = CartItem.objects.filter(user=user)
    for item in db_cart_items:
        product_id = str(item.product.id)
        session_cart[product_id] = session_cart.get(product_id, 0) + item.quantity
    request.session['cart'] = session_cart


