from datetime import datetime
from django.db.models import Q
from django.shortcuts import render, HttpResponse
from . models import Employee, Role, Department
from django.contrib import messages 
from django.shortcuts import redirect
from .models import Attendance
from .forms import AttendanceForm

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')


def index(request):
    return render(request, 'index.html')

def all(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'view.html', context)

def add(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'].replace(' ', ''))
        dept = int(request.POST['dept'])
        role = int(request.POST['role'])
        location = request.POST['location']

        new_emp = Employee(
            first_name=first_name,
            last_name=last_name,
            salary=salary,
            bonus=bonus,
            phone=phone,
            dept_id=dept,
            role_id=role,
            location=location,
            hire_date=datetime.now()
        )
        new_emp.save()
        messages.success(request, 'Employee added successfully!')

        return redirect('all')
     
    elif request.method == "GET":
        departments = Department.objects.all()
        roles = Role.objects.all()
        locations = Department.objects.distinct()

        context = {
            'departments': departments,
            'roles': roles,
            'locations': locations,
        }
        return render(request, "add.html", context)
    else:
        return HttpResponse("An exception occurred! Employee has not been added!")


    

def remove(request, emp_id = 0):
    if emp_id:
        try:
            emp_delete = Employee.objects.get(id=emp_id)
            emp_delete.delete()
            return redirect('remove') 
        except:
            return HttpResponse("Oops! Something went wrong.")
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'remove.html', context)
    
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_list') 
    else:
        form = AttendanceForm()
    return render(request, 'attendance/mark_attendance.html', {'form': form})

def attendance_list(request):
    attendance = Attendance.objects.all().order_by('-date')
    return render(request, 'attendance/attendance_list.html', {'attendance': attendance})



def filter(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        dept = request.POST.get('dept', '').strip()
        role = request.POST.get('role', '').strip()

        print(f"Received Name: {name}, Department: {dept}, Role: {role}")

        emps = Employee.objects.all()

        if name:
            name_parts = name.split()
            if len(name_parts) == 2:
                first, last = name_parts
                emps = emps.filter(
                    Q(first_name__icontains=first, last_name__icontains=last) |
                    Q(first_name__icontains=first) |
                    Q(last_name__icontains=last)
                )
            else:
                emps = emps.filter(
                    Q(first_name__icontains=name) | Q(last_name__icontains=name)
                )

        if dept:
            emps = emps.filter(dept__name__icontains=dept)
        if role:
            emps = emps.filter(role__name__icontains=role)

        print(f"Found employees: {emps}")

        context = {
            'emps': emps
        }
        return render(request, 'filter.html', context)

    else:
        emps = Employee.objects.none()
        context = {
            'emps': emps
        }
        return render(request, 'filter.html', context)
