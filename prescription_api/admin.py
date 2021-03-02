from django.contrib import admin
from .models import Doctor, Drug, Pharmacy, Booking, User

# Register your models here.

admin.site.register(Doctor)
admin.site.register(Drug)
admin.site.register(Pharmacy)
admin.site.register(Booking)
admin.site.register(User)
