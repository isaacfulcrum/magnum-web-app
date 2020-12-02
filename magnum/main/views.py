from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList
from .forms import create_list
# Create your views here.


def index(response, id):
    ls = ToDoList.objects.get(id=id)

    if not response.user.is_authenticated:
        return render(response, "main/list.html", {})

    if ls in response.user.todolist.all():

        if response.method == "POST":
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    if response.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()

            elif response.POST.get("new_item"):
                text = response.POST.get("new_text")
                if(len(text) > 2):
                    ls.item_set.create(text=text, complete=False)
                else:
                    print("Invalid input")

        percent = ls.item_set.count()
        if percent == 0:
            return render(response, "main/list.html", {"ls": ls})

        counter = 0
        for item in ls.item_set.all():
            if item.complete:
                counter += 1

        counter *= 100
        percent = counter//percent

        return render(response, "main/list.html", {"ls": ls, "percent": percent})

    return render(response, "main/view.html", {})


def home(response):
    return render(response, "main/base.html", {})


def create(response):
    if response.method == "POST":
        form = create_list(response.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            response.user.todolist.add(t)

        return HttpResponseRedirect("/{}".format(t.id))

    else:
        form = create_list()

    return render(response, "main/create.html", {"form": form})
