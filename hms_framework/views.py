import datetime

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from .factory import BookingFactory, CustomerFactory
from .forms import BookingForm
from .models import RoomType, Room, Country, City, Address, Customer, Booking, Invoice, InvoiceItem, InvoicePayment
from .services.booking.search_availability import SearchAvailability


def login_user(request):

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('birthdayreminder.views.main')

    return render(None, 'login.html', {'username': ''})


@login_required
def index(request):
    return render(request, 'dashboard/index.html', {})\


@login_required
def logout_view(request):
    logout(request)


@login_required
def new_booking(request, room_id=None, date_from=None, date_to=None):
    if request.method == "POST":
        model = BookingFactory().create_model()
        booking = model()
        booking.room = Room.objects.get(pk=request.POST.get('room'))
        booking.customer = Customer.objects.get(pk=request.POST.get('customer'))
        booking.date_from = request.POST.get('date_from')
        booking.date_to = request.POST.get('date_to')
        booking.created_by_id = request.user.id
        booking.save()

        return render(request, 'dashboard/index.html')

    if room_id and date_from and date_to:
        data = {'room': Room.objects.get(pk=room_id),
                'room_id': room_id,
                'date_from': date_from,
                'date_to': date_to}
    else:
        data = {}

    form = BookingForm(initial=data)

    return render(request, 'booking/new_booking.html', {
        'form': form,
        'room_id': room_id,
        'date_from': date_from,
        'date_to': date_to,
        'countries': Country.objects.all(),
        'cities': City.objects.all(),
    })


@login_required
def search_availability(request):

    room_types = RoomType.objects.all()

    if request.method == "POST":
        room_type = request.POST.get("room_type", "")
        number_of_guests = request.POST.get("number_of_guests", "")
        date_from = request.POST.get("date_from", "")
        date_to = request.POST.get("date_to", "")

        rooms = SearchAvailability(
            room_type=room_type,
            number_of_guests=number_of_guests,
            date_from=date_from,
            date_to=date_to,
        ).execute()

        if rooms is None:
            return render(request, 'booking/search_availability.html', {
                'room_types': room_types,
                'warning_message': 'NO_ROOM_FOUND',
            })

        return render(request, 'booking/search_availability.html', {
                'room_types': room_types,
                'rooms': rooms,
                'date_from': date_from,
                'date_to': date_to,
                'number_of_guests': number_of_guests,
                'selected_room_type': int(room_type)
            })

    return render(request, 'booking/search_availability.html', {'room_types': room_types})


@login_required
def checkin(request):
    # Get bookings whose checkin date is today
    bookings = Booking.objects.all()
    return render(request, 'booking/checkin.html', {'bookings': bookings})


@login_required
def checkin_open_dialog(request):
    if request.method != "POST":
        raise Exception('Request method is not supported.')

    booking_model = BookingFactory().create_model()
    booking = booking_model.objects.get(pk=request.POST.get('bookingId'))

    try:
        invoice = Invoice.objects.get(customer_id=booking.customer.id)
        invoice_items = InvoiceItem.objects.filter(invoice=invoice.id)
    except Invoice.DoesNotExist:

        invoice = Invoice()
        invoice.customer = booking.customer
        invoice.due_date = datetime.datetime.now()
        invoice.is_deleted = False
        invoice.created_by = User.objects.get(pk=request.user.id)
        invoice.save()

        invoice_item = InvoiceItem()
        invoice_item.amount = booking.total_amount
        invoice_item.description = str(booking.room) + ' (' + booking.date_from.strftime('%d/%m/%Y') + ' to ' + booking.date_to.strftime('%d/%m/%Y') +')'
        invoice_item.discount = 0
        invoice_item.invoice = invoice
        invoice_item.created_by_id = request.user.id
        invoice_item.save()
        invoice = Invoice.objects.get(customer_id=booking.customer.id)
        invoice_items = InvoiceItem.objects.filter(invoice_id=invoice.id)

    try:
        invoice_payments = InvoicePayment.objects.filter(invoice=invoice)
    except InvoicePayment.DoesNotExist:
        invoice_payments = None

    return render(request, 'booking/checkin_dialog.html', {
        'booking': booking,
        'invoice': invoice,
        'invoice_items': invoice_items,
        'invoice_payments': invoice_payments,
    })


@login_required
def checkin_mark_payment(request):
    if request.method != "POST":
        raise Exception('Request method is not supported.')

    payment_type = request.POST.get("type", "")
    invoice_id = request.POST.get("invoiceId", "")

    invoice_payment = InvoicePayment()
    invoice_payment.invoice = Invoice.objects.get(pk=int(invoice_id))
    invoice_payment.amount = invoice_payment.invoice.invoice_items_total()
    invoice_payment.payment_type = payment_type
    invoice_payment.created_by = User.objects.get(pk=request.user.id)
    invoice_payment.save()

    return JsonResponse({})


@login_required
def checkout(request):
    return render(request, 'booking/checkout.html', {})


@login_required
def occupancy_report(request):
    return render(request, 'report/occupancy_report.html', {})


@login_required
def save_customer_json(request):
    if not request.method == 'POST':
        raise Exception('Request type not supported.')

    model = CustomerFactory().create_model()
    customer = model()
    customer.first_name = request.POST.get("firstName", "")
    customer.last_name = request.POST.get("lastName", "")
    customer.telephone = request.POST.get("telephone", "")
    customer.email = request.POST.get("email", "")

    address = Address()
    address.house_number = request.POST.get("houseNumber", "")
    address.street = request.POST.get("street", "")
    address.postal_code = request.POST.get("postalcode", "")
    city_id = request.POST.get("city", "")
    address.city = City.objects.get(pk=city_id)
    country_id = request.POST.get("country", "")
    address.country = Country.objects.get(pk=country_id)
    address.created_by_id = request.user.id
    address.save()

    customer.address = address
    customer.created_by_id = request.user.id
    customer.save()
    customer_value = customer.id
    customer_label = str(customer)

    return JsonResponse({
        'customerValue': customer_value,
        'customerLabel': customer_label
    })