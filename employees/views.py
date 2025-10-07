from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Employee


def home(request):
    """Главная страница с описанием проекта и карточками сотрудников"""
    employees = Employee.objects.all()[:6]
    context = {
        "employees": employees,
        "title": "Главная - Система управления сотрудниками",
    }
    return render(request, "employees/home.html", context)


def employee_list(request):
    """Список всех сотрудников"""
    employees = Employee.objects.all()
    context = {
        "employees": employees,
        "title": "Все сотрудники",
    }
    return render(request, "employees/employee_list.html", context)


@login_required
def employee_detail(request, pk):
    """Подробная карточка сотрудника (только для авторизованных)"""
    employee = get_object_or_404(Employee, pk=pk)
    context = {
        "employee": employee,
        "title": f"{employee.full_name()} - Карточка сотрудника",
    }
    return render(request, "employees/employee_detail.html", context)


def project_description(request):
    """Страница с описанием проекта"""
    context = {
        "title": "О проекте - Система управления сотрудниками",
    }
    return render(request, "employees/project_description.html", context)
