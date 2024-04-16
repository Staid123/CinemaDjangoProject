from django.contrib import admin

from orders.models import Order, OrderProductItem, OrderTicketItem

# admin.site.register(Order)
# admin.site.register(OrderItem)

class OrderProductItemTabulareAdmin(admin.TabularInline):
    model = OrderProductItem
    fields = "product", "price", "quantity"
    search_fields = (
        "product",
    )
    extra = 0


@admin.register(OrderProductItem)
class OrderProductItemAdmin(admin.ModelAdmin):
    list_display = "order", "product", "price", "quantity"
    search_fields = (
        "order",
        "product",
    )

class OrderTicketItemTabulareAdmin(admin.TabularInline):
    model = OrderTicketItem
    fields = "ticket", "price",
    search_fields = (
        "ticket",
    )
    extra = 0


@admin.register(OrderTicketItem)
class OrderTicketItemAdmin(admin.ModelAdmin):
    list_display = "order", "ticket", "price"
    search_fields = (
        "order",
        "ticket",
    )


class OrderTabulareAdmin(admin.TabularInline):
    model = Order
    fields = (
        "created_timestamp",
        "phone_number",
        "email"
    )

    search_fields = (
        "created_timestamp",
    )
    readonly_fields = ("created_timestamp",)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "created_timestamp",
    )

    search_fields = (
        "id",
    )
    readonly_fields = ("created_timestamp",)
    inlines = (OrderProductItemTabulareAdmin, OrderTicketItemTabulareAdmin)