from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Skill(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название навыка")

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name


class EmployeeSkill(models.Model):
    employee = models.ForeignKey(
        "Employee", on_delete=models.CASCADE, verbose_name="Сотрудник"
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


class Employee(models.Model):
    GENDER_CHOICES = [
        ("M", "Мужской"),
        ("F", "Женский"),
        ("O", "Другой"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        null=True,
        blank=True,
    )
    middle_name = models.CharField(max_length=50, blank=True, verbose_name="Отчество")
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, null=True, verbose_name="Пол"
    )
    skills = models.ManyToManyField(
        Skill, through=EmployeeSkill, verbose_name="Навыки", blank=True
    )
    description = models.TextField(verbose_name="Описание", blank=True)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name} {self.middle_name or ''}".strip()

    def full_name(self):
        return f"{self.user.last_name} {self.user.first_name} {self.middle_name or ''}".strip()

    def get_skills_with_levels(self):
        """Возвращает навыки с уровнями"""
        return ", ".join(
            [f"{es.skill.name} ({es.level})" for es in self.employeeskill_set.all()]
        )


@receiver(post_save, sender=User)
def create_employee(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_employee(sender, instance, **kwargs):
    instance.employee.save()
