from django.urls import path
from AppCitas import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('', views.home, name='home-page'), 
    path('services/', views.ServicesListView.as_view(), name='services-list'),
    path('services/new/', views.ServicesCreateView.as_view(), name='services-create'),
    path('services/<int:pk>/update/', views.ServicesUpdateView.as_view(), name='services-update'),
    path('services/<int:pk>/delete/', views.ServicesDeleteView.as_view(), name='services-delete'),
    path('doctor_services/', views.DoctorServicesListView.as_view(), name='doctor-services-list'),
    path('doctor_services/new/', views.DoctorServicesCreateView.as_view(), name='doctor-services-create'),
    path('doctor_services/<int:pk>/update/', views.DoctorServicesUpdateView.as_view(), name='doctor-services-update'),
    path('doctor_services/<int:pk>/delete/', views.DoctorServicesDeleteView.as_view(), name='doctor-services-delete'),
    path('doctor_time_slots/', views.DoctorTimeSlotsListView.as_view(), name='doctor-time-slots-list'),
    path('doctor_time_slots/new/', views.DoctorTimeSlotsCreateView.as_view(), name='doctor-time-slots-create'),
    path('doctor_time_slots/<int:pk>/update/', views.DoctorTimeSlotsUpdateView.as_view(), name='doctor-time-slots-update'),
    path('doctor_time_slots/<int:pk>/delete/', views.DoctorTimeSlotsDeleteView.as_view(), name='doctor-time-slots-delete'),
    path('appointments/', views.AppointmentsListView.as_view(), name='appointments-list'),
    path('appointments/new/', views.AppointmentsCreateView.as_view(), name='appointments-create'),
    path('appointments/<int:pk>/update/', views.AppointmentsUpdateView.as_view(), name='appointments-update'),
    path('appointments/<int:pk>/delete/', views.AppointmentsDeleteView.as_view(), name='appointments-delete'),
]