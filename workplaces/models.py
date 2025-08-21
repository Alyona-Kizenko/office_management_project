from django.db import models
from employees.models import Employee


class Workplace(models.Model):
    desk_number = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="Номер стола"
    )
    description = models.TextField(
        verbose_name="Дополнительная информация", 
        blank=True
    )
    employee = models.OneToOneField(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Сотрудник",
        related_name="workplace"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Создано"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Обновлено"
    )

    class Meta:
        verbose_name = "Рабочее место"
        verbose_name_plural = "Рабочие места"
        ordering = ["desk_number"]

    def __str__(self):
        if self.employee:
            return f"Стол {self.desk_number} - {self.employee}"
        return f"Стол {self.desk_number} (свободен)"