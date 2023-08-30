from django.urls import path
from .views import (lab_login,lab_register,patient_register,patient_login,create_bill,bill_report,edit_bill,patient_dashboard,bills_,download_bill)
from . import views
urlpatterns = [
    path('login/', lab_login, name='lab_login'),
    path('register/', lab_register, name='lab_register'),
    path('patient/', patient_register, name='patient_register'),
    path('patient_login/',patient_login,name='patient_login'),
    path('', lab_register, name='lab_register'),
    path('create_bill/',create_bill,name='create_bill'),
    path('bill_report/<int:bill_id>',bill_report,name='bill_report'),
    path('edit_bill/<int:bill_id>',edit_bill,name='edit_bill'),
    path('download_bill/<int:bill_id>/',download_bill,name='download_bill'),
     path('generate_pdf_response/<int:bill_id>/', views.generate_pdf_response, name='generate_pdf_response'),
    path('bills/',bills_,name='bills'),
    path('patient_dashboard/<int:bill_id>/', patient_dashboard, name='patient_dashboard'),

    

    
]
  