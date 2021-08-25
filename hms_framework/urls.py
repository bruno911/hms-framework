"""hotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework.documentation import include_docs_urls

from hms_framework import views, settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^booking/new_booking/(?P<room_id>[0-9]+)/(?P<date_from>[0-9-]+)/(?P<date_to>[0-9-]+)$',
        views.new_booking,
        name='new_booking_route_room'),
    url(r'^booking/new_booking', views.new_booking, name='new_booking_route'),
    url(r'^booking/checkin_mark_payment$', views.checkin_mark_payment, name='booking_checkin_mark_payment'),
    url(r'^booking/checkin_open_dialog$', views.checkin_open_dialog, name='booking_checkin_open_dialog'),
    url(r'^booking/checkin$', views.checkin, name='booking_checkin'),
    url(r'^booking/checkout', views.checkout, name='booking_checkout'),
    url(r'^search_availability', views.search_availability, name='search_availability'),
    url(r'^report/occupancy_report', views.occupancy_report, name='occupancy_report'),
    url(r'^api/customer/create', views.save_customer_json, name='save_customer_json'),
    url(r'^logout', auth_views.LogoutView, name='logout'),

    url(f'^accounts/login/', auth_views.LoginView, name='login'),

    # API
    path("api/v1/", include("hms_framework.api.urls")),
    url(r'^api/docs/', include_docs_urls(title='hms_framework')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += url(r'^$', views.index),

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)