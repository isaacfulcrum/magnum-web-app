from django.shortcuts import render, redirect
from .forms import register_form
# Create your views here.


def register(response):

    if response.method == "POST":
        form = register_form(response.POST)
        if form.is_valid():
            form.save()

        return redirect("/")
    else:
        form = register_form()
    return render(response, "register/register.html", {"form": form})
