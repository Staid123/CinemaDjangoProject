from django.contrib import admin

from .models import ProductCart, TicketCart

# admin.site.register(ProductCart)
# admin.site.register(TicketCart)

class ProductCartTabAdmin(admin.TabularInline):
    model = ProductCart
    fields = "product", "quantity", "created_timestamp"
    search_fields = "product", "quantity", "created_timestamp"
    readonly_fields = ("created_timestamp",)
    extra = 1


class TicketCartTabAdmin(admin.TabularInline):
    model = TicketCart
    fields = "ticket", "created_timestamp"
    search_fields = "ticket", "created_timestamp"
    readonly_fields = ("created_timestamp",)
    extra = 1


@admin.register(ProductCart)
class ProductCartsAdmin(admin.ModelAdmin):
    list_display = ["user_display", "product_display", "quantity", "created_timestamp"]
    list_filter = ["created_timestamp", "user", "product"]

    def product_display(self, obj):
        return str(obj.product.name)
    
    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return "Анонимный пользователь"
    


