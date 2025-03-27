import os
from django.shortcuts import render, redirect
from supabase import create_client
from decouple import config
from django.contrib import messages

LOCAL_API_KEY = config("API_KEY")
LOCAL_BASE_URL = config("BASE_URL")

API_KEY = os.environ.get("API_KEY", default=LOCAL_API_KEY)
BASE_URL = os.environ.get("BASE_URL", default=LOCAL_BASE_URL)

supabase = create_client(BASE_URL, API_KEY)


def get_logged_user():
    try:
        logged_user = supabase.auth.get_user()
        user_name = logged_user.user.user_metadata.get("full_name")

        return user_name

    except Exception as e:
        print(f"Error getting logged user: {e}")
        return False


def home(request):
    context = {
        "logged_user": get_logged_user()
    }

    return render(request, "home.html", context)


def tasks(request):
    logged_user = get_logged_user()

    context = {
        "logged_user": logged_user
    }

    if logged_user:
        try:
            tasks = supabase.table("task").select("*").execute()

            context["tasks"] = tasks.data

        except Exception as e:
            print(f"Error selecting tasks: {e}")
            messages.error(request, "Error selecting tasks, please try again")

    return render(request, "tasks.html", context)


def add_task(request):
    if request.method == "POST":
        try:
            new_task = supabase.table("task").insert({
                "title": request.POST["title"],
                "description": request.POST["description"]
            }).execute()

            # Arreglaar esto de los mensajes pq me sale en el navbar siempre
            messages.success(request, "Task added succesfully!")

        except Exception as e:
            print(f"Error creating task: {e}")
            messages.error(request, "Error creating task, please try again")

    return redirect("tasks")


def mark_task_completed(request):
    if request.method == "POST":
        task_id = int(request.POST.get("task_id"))

        try:
            update_task = (
                supabase.table("task")
                .update({"completed": True}) #Probar aqui de todas maneras si no me actualiza el campo con otro usuario
                .eq("id", task_id)
                .execute()
            )

        except Exception as e:
            print(f"Error updating task: {e}")
            messages.error(request, "Error updating task, please try again")

    return redirect("tasks")


def delete_task(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id")

        try:
            delete_task = (
                supabase.table("task")
                .delete()
                .eq("id", task_id)
                .execute()
            )

        except Exception as e:
            print(f"Error deleting task: {e}")
            messages.error(request, "Error deleting task, please try again")

    return redirect("tasks")


def login_user(request):
    context = {}

    if request.method == "POST":
        user_email = request.POST.get("user_email")
        user_password = request.POST.get("user_password")

        try:
            login_user = supabase.auth.sign_in_with_password({
                "email": user_email,
                "password": user_password
            })

            return redirect("home")

        except Exception as e:
            context["message"] = "Invalid login credentials"
            print(e)

    return render(request, "login.html", context)


def logout_user(request):
    try:
        supabase.auth.sign_out()

        return redirect("home")

    except Exception as e:
        print(f"Error closing session: {e}")
        messages.error(request, "Error closing session, please try again")
        return redirect("home")


def register(request):
    context = {}

    if request.method == "POST":

        try:
            new_user = supabase.auth.sign_up({
                "email": request.POST.get("user_email"),
                "password": request.POST.get("user_password"),
                "options": {
                    "data": {
                        "full_name": request.POST.get("user_name")
                    }
                }
            })

            return redirect("home")

        except Exception as e:
            context["message"] = "Error creating user, please try again"
            print(f"Error creating user: {e}")

    return render(request, "register.html", context)
