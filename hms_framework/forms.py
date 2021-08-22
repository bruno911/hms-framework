from django import forms
from django.forms import ModelForm, Select

# This code will transform a Model into a Form.
from .models import Room, Customer, Booking


class BookingForm(ModelForm):
    date_from = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date', 'class': 'form-control'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date', 'class': 'form-control'}))
    room = forms.ChoiceField(choices=[],
                             widget=Select(attrs={'class': 'form-control'}))
    customer = forms.ChoiceField(choices=[],
                                 widget=Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choice_list = [(room.id, str(room)) for room in Room.objects.all()]
        self.fields['room'].choices = choice_list
        choice_list = [(customer.id, str(customer)) for customer in Customer.objects.all()]
        self.fields['customer'].choices = choice_list

    class Meta:
        model = Booking
        fields = ['room', 'customer', 'date_from', 'date_to']

