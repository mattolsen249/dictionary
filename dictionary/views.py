from django.shortcuts import render
from django.core.cache import cache
from . import utils


def index(request):
    return render(request, "index_page.html")


def words_list(request):
    words = utils.get_words_for_table()
    return render(request, "show_word_list_page.html", context={"words": words})


def add_word(request):
    return render(request, "add_word_page.html")


def send_word(request):
    if request.method == "POST":
        cache.clear()
        email = request.POST.get("email")
        word = request.POST.get("word", "")
        translation = request.POST.get("translation", "")
        context = {}
        if len(word) == 0:
            context["success"] = False
            context["comment"] = "Поле \"Слово\" не должно быть пустым"
        elif len(translation) == 0:
            context["success"] = False
            context["comment"] = "Поле \"Перевод\" не должно быть пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваша запись принята"
            utils.write_word(word, translation, email)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "add_word_res_page.html", context)
    else:
        add_word(request)


def show_stats(request):
    stats = utils.get_words_stats()
    return render(request, "show_stats_page.html", stats)
