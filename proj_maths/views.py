from django.shortcuts import render
from django.core.cache import cache
from . import terms_work, tasks_work


def index(request):
    return render(request, "index.html")


def terms_list(request):
    terms = terms_work.get_terms_for_table()
    return render(request, "term_list.html", context={"terms": terms})


def add_term(request):
    return render(request, "term_add.html")


def send_term(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_term = request.POST.get("new_term", "")
        new_definition = request.POST.get("new_definition", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_definition) == 0:
            context["success"] = False
            context["comment"] = "Перевод не должен быть пустым"
        elif len(new_term) == 0:
            context["success"] = False
            context["comment"] = "Слово не должно быть пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваше слово принято"
            terms_work.write_term(new_term, new_definition)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "term_request.html", context)
    else:
        add_term(request)


def show_stats(request):
    stats = terms_work.get_terms_stats()
    return render(request, "stats.html", stats)


def tasks_list(request):
    terms = tasks_work.get_tasks_for_table()
    return render(request, "task_list.html", context={"terms": terms})


def add_task(request):
    return render(request, "task_add.html")


def send_task(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_term = request.POST.get("new_term", "")
        new_definition = request.POST.get("new_definition", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_definition) == 0:
            context["success"] = False
            context["comment"] = "Задание не должно быть пустым"
        elif len(new_term) == 0:
            context["success"] = False
            context["comment"] = "Номер задания не должен быть пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваше задание принято"
            tasks_work.write_task(new_term, new_definition)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "task_request.html", context)
    else:
        add_task(request)


def show_progress(request):
    stats = tasks_work.get_tasks_stats()
    return render(request, "progress.html", stats)
