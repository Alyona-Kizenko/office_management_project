import os
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone


class Skill(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название навыка")

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name


class Employee(models.Model):
    GENDER_CHOICES = [
        ("M", "Мужской"),
        ("F", "Женский")
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        null=True,
        blank=True,
    )
    first_name = models.CharField(max_length=50, verbose_name="Имя", blank=True)
    last_name = models.CharField(max_length=50, verbose_name="Фамилия", blank=True)
    middle_name = models.CharField(max_length=50, blank=True, verbose_name="Отчество")
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, null=True, verbose_name="Пол"
    )
    skills = models.ManyToManyField(
        Skill, through="EmployeeSkill", verbose_name="Навыки", blank=True
    )
    description = models.TextField(verbose_name="Описание", blank=True)
    hire_date = models.DateField(
        verbose_name="Дата приёма на работу", 
        default=timezone.now,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name or ''}".strip()

    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name or ''}".strip()

    def get_skills_display(self):
        """Возвращает строку с навыками и уровнями"""
        skills = self.employeeskill_set.all()
        if skills:
            return ", ".join([f"{es.skill.name} ({es.level})" for es in skills])
        return "Нет навыков"


class EmployeeSkill(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name="Сотрудник"
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, verbose_name="Навык")
    level = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)], verbose_name="Уровень навыка"
    )

    class Meta:
        verbose_name = "Навык сотрудника"
        verbose_name_plural = "Навыки сотрудников"
        unique_together = ["employee", "skill"]

    def __str__(self):
        return f"{self.employee} - {self.skill} (уровень {self.level})"


class EmployeeImage(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name="Сотрудник",
        related_name="images",
    )
    image = models.ImageField(
        upload_to="employee_images/", verbose_name="Изображение"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядковый номер")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Изображение сотрудника"
        verbose_name_plural = "Изображения сотрудников"
        ordering = ["order"]

    def __str__(self):
        return f"Изображение {self.order} для {self.employee}"

    def delete(self, *args, **kwargs):
        """Удаляем файл с диска при удалении объекта"""
        import os
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)


# Сигналы
@receiver(post_save, sender=User)
def create_employee(sender, instance, created, **kwargs):
    """Создаём объект Employee при создании User"""
    if created:
        Employee.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_employee(sender, instance, **kwargs):
    """Сохраняем Employee при сохранении User"""
    if hasattr(instance, 'employee'):
        instance.employee.save()


@receiver(pre_delete, sender=EmployeeImage)
def delete_employee_image_file(sender, instance, **kwargs):
    """Удаляем файл изображения при удалении объекта из БД"""
    import os
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)