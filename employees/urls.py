from django.urls import path
from . import views

app_name = "employees"

urlpatterns = [
    path("", views.home, name="home"),
    path("list/", views.employee_list, name="employee_list"),
    path("<int:pk>/", views.employee_detail, name="employee_detail"),
    path("about/", views.project_description, name="project_description"),
]
