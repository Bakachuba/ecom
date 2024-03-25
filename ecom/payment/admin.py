from django.contrib import admin

from payment.models import ShippingAddress, Order, OrderItem

# register the model on the admin section thing
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)