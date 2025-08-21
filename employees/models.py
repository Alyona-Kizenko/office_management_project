from django.db import models

from workplaces.models import Workplace


class Employee(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    position = models.CharField(max_length=100, verbose_name="Должность")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    workplace = models.ForeignKey(
        Workplace,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Рабочее место",
    )
    hire_date = models.DateField(verbose_name="Дата приема на работу")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
