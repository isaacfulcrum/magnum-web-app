from django.shortcuts import render, redirect
from .forms import register_form
from django.contrib import messages

# Create your views here.


def register(response):

    if response.method == "POST":
        form = register_form(response.POST)
        if form.is_valid():
            form.save()
        else:
            for msg in form.error_messages:
                messages.error(response, f"{msg}: {form.error_messages[msg]}")
    else:
        form = register_form()
    return render(response, "register/register.html", {"form": form})
