from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Hotel)
admin.site.register(models.City)
admin.site.register(models.Country)
admin.site.register(models.Address)


class RoomAdmin(admin.ModelAdmin):
    save_as = True


admin.site.register(models.Room, RoomAdmin)
admin.site.register(models.RoomType)
admin.site.register(models.BedType)
admin.site.register(models.RoomFeatureType)
admin.site.register(models.RoomTypePicture)
admin.site.register(models.RoomPricePeriod)
admin.site.register(models.Customer)
admin.site.register(models.Invoice)
admin.site.register(models.InvoiceItem)
admin.site.register(models.InvoicePayment)
admin.site.register(models.Booking)
