from django.contrib import admin
from .models import *

class CustomerAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'name', 'email')
  list_display_links = ('user',)
  ordering = ['name', 'user']

class ProductAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'price', 'is_promo', 'tag')
  list_display_links = ('name',)
  ordering = ['id',]

  

class OrderAdmin(admin.ModelAdmin):
  list_display = ('id', 'customer', 'date_ordered', 'complete')

class OrderItemAdmin(admin.ModelAdmin):
  list_display = ('product', 'order', 'quantity', 'date_added')
  list_display_links = ('product', 'order')
  
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('id', 'name')

class TagAdmin(admin.ModelAdmin):
  list_display = ('id', 'name')

class MessageAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'archive')

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(BackgroundImage)
admin.site.register(Msg, MessageAdmin)