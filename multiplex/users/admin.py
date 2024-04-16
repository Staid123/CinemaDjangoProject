from django.contrib import admin

from carts.admin import ProductCartTabAdmin, TicketCartTabAdmin
from orders.admin import OrderTabulareAdmin
from .models import User


# admin.site.register(User)

@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'username', 'email', 'phone_number']
    search_fields = ["username", "first_name", "last_name", "email"]
    inlines = [ProductCartTabAdmin, TicketCartTabAdmin, OrderTabulareAdmin]