from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tasks/", views.tasks, name="tasks"),
    path("add_task/", views.add_task, name="add_task"),
    path("mark_task_completed/", views.mark_task_completed, name="mark_task_completed"),
    path("delete_task/", views.delete_task, name="delete_task"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register, name="register")
]
