from django.contrib import admin
from .models import Profile


from django.apps import AppConfig

class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MainApp'

    def ready(self):
        import MainApp.signals  # 👈 important

# Register your models here.
from django.contrib import admin
from .models import Category, Product, CartItem, Order

admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(Order)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_featured', 'is_new')
    list_editable = ('is_featured', 'is_new')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'gender', 'city','age','region_state','district']


from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'gateway', 'order_id', 'amount', 'status', 'created_at')
    list_filter = ('status', 'gateway')
    search_fields = ('order_id', 'user__username')

