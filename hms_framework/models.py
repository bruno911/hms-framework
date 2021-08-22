from django.contrib.auth.models import User
from django.db import models
# Hotel - Model:
# id: int
# name: string
# address_id: Address
# currency_code: string (example: 'EUR')
# created_by_user_id: User
# created_datetime: datetime
# Capabilities:
# getListOfAvailableRooms()
from django_resized import ResizedImageField
from django.forms import model_to_dict


class Hotel(models.Model):

    def __str__(self):
        return f"{self.id}-{self.name}"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.ForeignKey('Address', on_delete=models.PROTECT)
    currency_code = models.CharField(max_length=3)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created_datetime = models.DateTimeField(auto_now_add=True)

    def get_list_of_available_rooms(self):
        # TODO:
        pass


# Address - Model:
# house_number: string
# street: string
# city_id: City
# country_id: Country
# postal_code: string
# created_by_user_id: User
# created_datetime: datetime

class Address(models.Model):

    # String representation
    def __str__(self):
        return f"{self.id}-{self.street}"

    id = models.AutoField(primary_key=True)
    house_number = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.ForeignKey('City', on_delete=models.PROTECT)
    country = models.ForeignKey('Country', on_delete=models.PROTECT)

    postal_code = models.CharField(max_length=10)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created_datetime = models.DateTimeField(auto_now_add=True)


# City - Model:
# id: int
# country_id: Country
# name: string


class City(models.Model):

    # String representation
    def __str__(self):
        return f"{self.name}"

    id = models.AutoField(primary_key=True)
    country = models.ForeignKey('Country', on_delete=models.PROTECT)
    name = models.CharField(max_length=255)


# Country - Model:
# id: int
# name: string
# phone_prefix: string(example: +353
# for Ireland)


class Country(models.Model):

    # String representation
    def __str__(self):
        return f"{self.name}"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone_prefix = models.CharField(max_length=4)


# Room - Model:
# id: id
# hotel_id: Hotel
# price_night: float
# price_week: float
# price_month: float
# type externalinternal
# description: string,
# room_number: int
# floor: int
# square_meters: int
# created_by_user_id: User
# created_datetime: datetime
# .... any other things that could make part of a room. Maybe Dave/Iggy will have more about the business model of a hotel.
# Capabilities:
# isRoomAvailable() (we will provide the date from and date to to know if this room can be booked)

class Room(models.Model):
    # String representation
    def __str__(self):
        return f"{self.room_type.name} - Floor: {self.floor} - Room: {self.room_number}"

    hotel = models.ForeignKey('Hotel', on_delete=models.PROTECT)
    price_night = models.IntegerField()  # 100 = 1.00
    price_week = models.IntegerField()  # 100 = 1.00
    price_month = models.IntegerField()  # 100 = 1.00
    room_type = models.ForeignKey('RoomType', on_delete=models.PROTECT)
    description = models.CharField(max_length=255)
    room_number = models.IntegerField()
    floor = models.IntegerField()
    square_meters = models.IntegerField()  # 100 = 1.00
    room_features = models.ManyToManyField('RoomFeatureType')
    room_beds = models.ManyToManyField('BedType')
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created_datetime = models.DateTimeField(auto_now_add=True)


class RoomType(models.Model):

    def __str__(self):
        return f"{self.name}"

    name = models.CharField(max_length=255)
    pictures = models.ManyToManyField('RoomTypePicture')


class RoomFeatureType(models.Model):

    def __str__(self):
        return f"{self.name}"

    name = models.CharField(max_length=255)
    is_everywhere = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created_datetime = models.DateTimeField(auto_now_add=True)


# two Queen, King size, single, cot for a baby
class BedType(models.Model):

    def __str__(self):
        return f"{self.name}"

    name = models.CharField(max_length=255)
    people_capacity = models.IntegerField(default=1)


class RoomTypePicture(models.Model):
    image = ResizedImageField(size=[500, 500],
                              crop=['middle', 'center'],
                              upload_to='images/rooms/')


class RoomPricePeriod(models.Model):

    def __str__(self):
        return f"{self.valid_date_from} - {self.valid_date_to}"

    room = models.ForeignKey('Room', on_delete=models.PROTECT)
    price_night = models.IntegerField()  # 100 = 1.00
    price_week = models.IntegerField()  # 100 = 1.00
    price_month = models.IntegerField()  # 100 = 1.00
    valid_date_from = models.DateField()
    valid_date_to = models.DateField()
    VALID_TYPE_CHOICES = (
        ('BOOKING_DATE', 'Booking Date'),
        ('STAY_DATE', 'Stay Date')
    )
    valid_type = models.CharField(
        choices=VALID_TYPE_CHOICES,
        max_length=100
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created_datetime = models.DateTimeField(auto_now_add=True)


class CustomerMemento(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT)
    field_name = models.CharField(max_length=255)
    field_value = models.CharField(max_length=255)
    memento_datetime = models.DateTimeField(auto_now_add=True)


class Customer(models.Model):

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.ForeignKey('Address', on_delete=models.PROTECT)
    has_debts = models.BooleanField(default=False)
    last_has_debts_notified_datetime = models.DateTimeField(auto_now_add=False, blank=True, null=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    @property
    def _dict(self):
        _dict = model_to_dict(self, fields=[field.name for field in
                              self._meta.fields])
        return _dict

    def save_memento(self):
        if self.has_changed:
            for field_name in self.changed_fields:
                # Id will change on creation only, so we ignore this.
                if field_name == 'id':
                    continue
                customer_memento = CustomerMemento()
                customer_memento.customer = self
                customer_memento.field_name = field_name
                customer_memento.field_value = self._dict[field_name]
                customer_memento.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        self.save_memento()
        self.__initial = self._dict

    def undo(self, customer_memento: CustomerMemento):
        if self.id != customer_memento.customer.id:
            raise Exception('Customer memento does not match current customer')
        setattr(self, customer_memento.field_name, customer_memento.field_value)
        super().save()


class Invoice(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT)
    due_date = models.DateField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created_datetime = models.DateTimeField(auto_now_add=True)

    def invoice_items_total(self):
        try:
            total = 0
            invoice_items = InvoiceItem.objects.filter(invoice=self)
            for invoice_item in invoice_items:
                total += invoice_item.amount
        except InvoiceItem.DoesNotExist:
            return 0

        return total


class InvoiceItem(models.Model):
    invoice = models.ForeignKey('Invoice', on_delete=models.PROTECT)
    description = models.CharField(max_length=255)
    amount = models.IntegerField()  # 100 = 1.00
    discount = models.IntegerField()  # 100 = 1.00
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created_datetime = models.DateTimeField(auto_now_add=True)


class InvoicePayment(models.Model):
    invoice = models.ForeignKey('Invoice', on_delete=models.PROTECT)
    amount = models.IntegerField()  # 100 = 1.00
    PAYMENT_TYPE_CHOICES = (
        ('CARD', 'Card'),
        ('CASH', 'Cash')
    )
    payment_type = models.CharField(
        choices=PAYMENT_TYPE_CHOICES,
        max_length=100
    )
    comments = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created_datetime = models.DateTimeField(auto_now_add=True)


class Booking(models.Model):
    room = models.ForeignKey('Room', on_delete=models.PROTECT)
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT)
    date_from = models.DateField()
    date_to = models.DateField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created_datetime = models.DateTimeField(auto_now_add=True)

    @property
    def total_amount(self):
        delta = self.date_to - self.date_from
        days = delta.days

        if days <= 31:
            total_amount = (self.room.price_month / 31) * days
        elif days <= 7:
            total_amount = (self.room.price_week / 7) * days
        else:
            total_amount = self.room.price_night * days

        return total_amount
