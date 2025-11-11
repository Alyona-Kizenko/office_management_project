from django.db import models
from django.core.exceptions import ValidationError
from employees.models import Employee

def validate_workplace_neighbors(employee, desk_number):
    """
    Валидатор, который не допускает нахождение тестировщиков 
    и разработчиков за соседними столами
    """
    # Проверяем является ли сотрудник тестировщиком или разработчиком
    is_tester = employee.skills.filter(name__icontains='тестировщик').exists()
    is_developer = employee.skills.filter(
        name__icontains='разработчик'
    ).exists() or employee.skills.filter(
        name__icontains='backend'
    ).exists() or employee.skills.filter(
        name__icontains='frontend'
    ).exists()
    
    if not (is_tester or is_developer):
        return  # Не тестировщик и не разработчик - проверка не нужна
    
    try:
        desk_num = int(desk_number)
    except (ValueError, TypeError):
        return  # Не числовой номер стола - пропускаем проверку
    
    # Проверяем соседние столы
    neighbor_desks = [desk_num - 1, desk_num + 1]
    
    from .models import Workplace
    neighbor_workplaces = Workplace.objects.filter(
        desk_number__in=[str(d) for d in neighbor_desks]
    ).exclude(employee=employee)
    
    for workplace in neighbor_workplaces:
        if workplace.employee:
            neighbor_is_tester = workplace.employee.skills.filter(
                name__icontains='тестировщик'
            ).exists()
            neighbor_is_developer = workplace.employee.skills.filter(
                name__icontains='разработчик'
            ).exists() or workplace.employee.skills.filter(
                name__icontains='backend'
            ).exists() or workplace.employee.skills.filter(
                name__icontains='frontend'
            ).exists()
            
            # Если текущий тестировщик, а сосед разработчик или наоборот
            if (is_tester and neighbor_is_developer) or (is_developer and neighbor_is_tester):
                raise ValidationError(
                    f"Тестировщики и разработчики не могут сидеть за соседними столами! "
                    f"Стол {workplace.desk_number} занят {workplace.employee.full_name()}"
                )

class Workplace(models.Model):
    desk_number = models.CharField(
        max_length=20, unique=True, verbose_name="Номер стола", blank=True, null=True
    )
    description = models.TextField(verbose_name="Дополнительная информация", blank=True)
    employee = models.OneToOneField(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Сотрудник",
        related_name="workplace",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Рабочее место"
        verbose_name_plural = "Рабочие места"
        ordering = ["desk_number"]

    def __str__(self):
        if self.employee:
            return f"Стол {self.desk_number} - {self.employee}"
        return f"Стол {self.desk_number} (свободен)"

    def clean(self):
        """Валидация при сохранении"""
        if self.employee and self.desk_number:
            validate_workplace_neighbors(self.employee, self.desk_number)
        super().clean()

    def save(self, *args, **kwargs):
        """Вызываем валидацию при сохранении"""
        self.full_clean()
        super().save(*args, **kwargs)