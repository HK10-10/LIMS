
from django.http import HttpResponse
from django.template.loader import get_template

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Lab, Patient, Bill, Test
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.db.models import Max
import pdfkit


def generate_pdf_response(template, context):
    template = get_template(template)
    html = template.render(context)
    pdf = pdfkit.from_string(html, False)

    filename = "patient_bill.pdf"

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="' + filename + '"'
    return response


def lab_register(request):
    if request.method == 'POST':
        try:
            User.objects.get(username=request.POST.get('username'))
            return render(request, 'register.html', {"error_message": "Username should be unique"})
        except User.DoesNotExist:
            user_data = {
                "username": request.POST.get('username'),
                "email": request.POST.get('email'),
                "password": make_password(request.POST.get('password'))
            }
            user = User.objects.create(**user_data)

        lab_data = {
            "user": user,
            "name": request.POST.get('name'),
            "pincode": request.POST.get('pincode'),
            "address": request.POST.get('address'),
            "state": request.POST.get('state')
        }
        Lab.objects.create(**lab_data)
        return redirect('lab_login')
    return render(request, 'register.html')


def lab_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('patient_register')
        else:
            error_message = "Invalid credentials. Please try again."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')


def patient_register(request):
    if request.method == 'POST':
        try:

            User.objects.get(username=request.POST.get('pname'))
            return render(request, 'patient.html', {"error_message": "already a registered patient"})
        except User.DoesNotExist:
            user_data = {
                "username": request.POST.get('pname'),
                "email": request.POST.get('email'),
                "password": make_password(request.POST.get('ppassword'))
            }
            user = User.objects.create(**user_data)
            lab = Lab.objects.get(user=request.user)

            patient_data = {
                "name": request.POST.get('pname'),
                "email": request.POST.get('email'),
                "aadhar_no": request.POST.get('aadhar_no'),
                "contact": request.POST.get("contact"),
                "user": user,
                "lab": lab,
            }
            Patient.objects.create(**patient_data)
            return redirect('create_bill')
    return render(request, 'patient.html')


def patient_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            latest_bill_id = Bill.objects.filter(
                patient__user=request.user).aggregate(Max('id'))['id__max']
            return redirect('bills')

        else:
            error_message = "Invalid credentials. Please try again."
            return render(request, 'patient_login.html', {'error_message': error_message})
    return render(request, 'patient_login.html')


def create_bill(request):
    if request.method == 'POST':
        patient_id = request.POST['patient_id']

        test_names = request.POST.getlist('test_name[]')
        test_prices = request.POST.getlist('test_price[]')
        test_quantities = request.POST.getlist('test_quantity[]')
        try:
            patient = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            return render(request, 'bill.html', {"error_message": "Patient Does not exist"})

        bill = Bill.objects.create(patient=patient)

        for name, price, quantity in zip(test_names, test_prices, test_quantities):
            test_data = {
                # "name":name,
                "status": False,
                "price": price,
                "quantity": quantity,
                "sub_total": round(float(price) * float(quantity), 2)

            }
            test = Test.objects.update_or_create(
                name=name, bill=bill, defaults=test_data)

        return redirect(f'/edit_bill/{bill.id}')

    patients = Patient.objects.all()
    return render(request, 'bill.html', {'patients': patients, })


def bill_report(request, bill_id):
    tests = Test.objects.filter(bill_id=bill_id)
    total = 0
    for test in tests:
        total += float(test.sub_total)

    return render(request, 'report.html', {'tests': tests, 'total': total})


def edit_bill(request, bill_id):
    try:
        bill = Bill.objects.get(pk=bill_id)
    except Bill.DoesNotExist:
        return render(request, 'report.html', {"error_message": "Bill Does not exist"})

    tests = Test.objects.filter(bill=bill)

    if request.method == 'POST':
        test_names = request.POST.getlist('test_name[]')
        test_prices = request.POST.getlist('test_price[]')
        test_quantities = request.POST.getlist('test_quantity[]')
        test_value = request.POST.getlist('test_value[]')

        for test, name, price, quantity in zip(tests, test_names, test_prices, test_quantities):
            test.name = name
            test.price = price
            test.quantity = quantity
            test.sub_total = round(float(price) * float(quantity), 2)
            test.save()

    return render(request, 'edit_report.html', {'tests': tests, 'bill': bill})


def patient_dashboard(request, bill_id):
    tests = Test.objects.filter(bill_id=bill_id)
    total = 0
    for test in tests:
        total += float(test.sub_total)
    bill = get_object_or_404(Bill, id=bill_id)
    tests = bill.test_set.all()

    # response = generate_pdf_response(template='patient_dashboard.html', context={'bill': bill, 'tests': tests,'total':total })
    # return response

    return render(request, 'report.html', {'bill': bill, 'tests': tests, 'total': total})


def bills_(request):
    bills = Bill.objects.filter(patient__user=request.user)
    bills_list = []
    for bill in bills:
        bill_tests = bill.test_set.all()
        bills_list.append({
            "bill": bill,
            "bill_tests": bill_tests
        })

    return render(request, 'bill_list.html', {'bills': bills_list})


def download_bill(request, bill_id):
    tests = Test.objects.filter(bill_id=bill_id)
    total = 0
    for test in tests:
        total += float(test.sub_total)
    bill = get_object_or_404(Bill, id=bill_id)
    tests = bill.test_set.all()

    response = generate_pdf_response(template='patient_dashboard.html', context={
                                     'bill': bill, 'tests': tests, 'total': total})
    return response

    # return render(request, 'report.html', {'bill': bill, 'tests': tests,'total':total })
