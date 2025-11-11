from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Employee


def home(request):
    """Главная страница с описанием проекта и карточками сотрудников"""
    total_employees = Employee.objects.count()
    latest_employees = Employee.objects.select_related('user').prefetch_related(
        'images', 'skills', 'employeeskill_set__skill'
    ).order_by('-hire_date')[:4]
    
    # Добавляем дополнительные данные для каждого сотрудника
    for employee in latest_employees:
        employee.staff_image = employee.images.first()
        if employee.hire_date:
            employee.work_experience = (timezone.now().date() - employee.hire_date).days
        else:
            employee.work_experience = 0
    
    context = {
        "employees": latest_employees,
        "total_employees": total_employees,
        "title": "Главная - Система управления сотрудниками",
    }
    return render(request, "employees/home.html", context)


def employee_list(request):
    """Список всех сотрудников с пагинацией"""
    employees_list = Employee.objects.select_related('user').prefetch_related(
        'images', 'skills', 'employeeskill_set__skill'
    ).all()
    # Добавляем дополнительные данные для каждого сотрудника
    for employee in employees_list:
        employee.staff_image = employee.images.first()
        if employee.hire_date:
            employee.work_experience = (timezone.now().date() - employee.hire_date).days
        else:
            employee.work_experience = 0
    
    paginator = Paginator(employees_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj,
        "title": "Все сотрудники",
    }
    return render(request, "employees/employee_list.html", context)


@login_required
def employee_detail(request, pk):
    """Подробная карточка сотрудника (только для авторизованных)"""
    employee = get_object_or_404(
        Employee.objects.select_related('user', 'workplace').prefetch_related(
            'images', 'skills', 'employeeskill_set__skill'
        ), 
        pk=pk
    )
    # Добавляем дополнительные данные для сотрудника
    employee.main_image = employee.images.first()
    if employee.hire_date:
        employee.work_experience = (timezone.now().date() - employee.hire_date).days
    else:
        employee.work_experience = 0
    
    # Галерея изображений без первого (если есть)
    gallery_images = employee.images.all()
    if gallery_images.count() > 1:
        employee.gallery_images = gallery_images[1:]
    else:
        employee.gallery_images = []
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
