from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from .factory import BookingFactory, CustomerFactory, AuthFactory, InvoiceFactory, InvoicePaymentFactory, \
    RoomTypeFactory, CountryFactory, CityFactory, RoomFactory, ChartFactory
from .forms import BookingForm
from .value_object.booking.create_customer_request import CreateCustomerRequest
from .value_object.financial.build_invoice_request import BuildInvoiceRequest


def login_user(request):

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        authentication_service = AuthFactory().create_service()
        is_a_valid_user = authentication_service.is_a_valid_user(username=username, password=password)
        if not is_a_valid_user:
            raise Exception('Invalid user please try again.')

    return render(None, 'login.html', {'username': ''})


@login_required
def index(request):
    return render(request, 'dashboard/index.html', {})


@login_required
def logout_view(request):
    logout(request)


@login_required
def new_booking(request, room_id=None, date_from=None, date_to=None):
    if request.method == "POST":
        make_booking = BookingFactory().make_booking_service()
        make_booking.execute(
            room_id=request.POST.get('room'),
            customer_id=request.POST.get('customer'),
            date_from=request.POST.get('date_from'),
            date_to=request.POST.get('date_to'),
            created_by_user_id=request.user.id
        )

        return render(request, 'dashboard/index.html')

    if room_id and date_from and date_to:
        data = {'room': RoomFactory().create_model().objects.get(pk=room_id),
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
        'countries': CountryFactory().create_model().objects.all(),
        'cities': CityFactory().create_model().objects.all(),
    })


@login_required
def search_availability(request):

    room_types = RoomTypeFactory().create_model().objects.all()

    if request.method == "POST":
        room_type = request.POST.get("room_type", "")
        number_of_guests = request.POST.get("number_of_guests", "")
        date_from = request.POST.get("date_from", "")
        date_to = request.POST.get("date_to", "")

        search_availability_service = BookingFactory().search_availability_service()
        rooms = search_availability_service.execute(
            room_type=room_type,
            number_of_guests=number_of_guests,
            date_from=date_from,
            date_to=date_to
        )

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
    booking_model = BookingFactory().create_model()
    bookings = booking_model.objects.all()
    return render(request, 'booking/checkin.html', {'bookings': bookings})


@login_required
def checkin_open_dialog(request):
    if request.method != "POST":
        raise Exception('Request method is not supported.')

    invoice_service = InvoiceFactory().build_invoice_service()
    build_invoice_request = BuildInvoiceRequest(
        booking_id=request.POST.get('bookingId'),
        created_by_user_id=request.user.id
    )
    build_invoice_response = invoice_service.execute(build_invoice_request=build_invoice_request)

    return render(request, 'booking/checkin_dialog.html', {
        'booking': build_invoice_response.booking,
        'invoice': build_invoice_response.invoice,
        'invoice_items': build_invoice_response.invoice_items,
        'invoice_payments': build_invoice_response.invoice_payments,
    })


@login_required
def checkin_mark_payment(request):
    if request.method != "POST":
        raise Exception('Request method is not supported.')

    payment_type = request.POST.get("type", "")
    invoice_id = request.POST.get("invoiceId", "")
    user_id = request.user.id
    mark_payment_service = InvoicePaymentFactory().mark_payment_service()
    mark_payment_service.execute(
        invoice_id=invoice_id,
        payment_type=payment_type,
        created_by_user_id=user_id
    )

    return JsonResponse({})


@login_required
def checkout(request):
    return render(request, 'booking/checkout.html', {})


@login_required
def occupancy_report(request):

    empty_rooms_chart_base64 = ChartFactory().empty_rooms_daily().base64_image()
    guests_daily_chart_base64 = ChartFactory().guests_daily().base64_image()

    return render(request, 'report/occupancy_report.html', {
        'empty_rooms_chart_base64': empty_rooms_chart_base64,
        'guests_daily_chart_base64': guests_daily_chart_base64
    })


@login_required
def save_customer_json(request):
    if not request.method == 'POST':
        raise Exception('Request type not supported.')

    create_customer_request = CreateCustomerRequest(
        customer_first_name=request.POST.get("firstName", ""),
        customer_last_name=request.POST.get("lastName", ""),
        customer_telephone=request.POST.get("telephone", ""),
        customer_email=request.POST.get("email", ""),
        address_house_number=request.POST.get("houseNumber", ""),
        address_street=request.POST.get("street", ""),
        address_postal_code=request.POST.get("postalcode", ""),
        address_city_id=request.POST.get("city", ""),
        address_country_id=request.POST.get("country", ""),
        created_by_user_id=request.user.id
    )
    create_customer_service = CustomerFactory().create_customer_service()
    create_customer_response = create_customer_service.execute(
        create_customer_request=create_customer_request
    )

    customer_value = create_customer_response.customer.id
    customer_label = str(create_customer_response.customer)

    return JsonResponse({
        'customerValue': customer_value,
        'customerLabel': customer_label
    })
