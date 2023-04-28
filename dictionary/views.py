from django.shortcuts import render
from django.core.cache import cache
from . import utils


def index(request):
    return render(request, "index_page.html")


def words_list(request):
    words = utils.get_words_for_table()
    return render(request, "show_word_list_page.html",
                  context={"words": words})


def add_word(request):
    return render(request, "add_word_page.html")


def send_word_add(request):
    if request.method == "POST":
        cache.clear()
        email = request.POST.get("email")
        word = request.POST.get("word", "")
        translation = request.POST.get("translation", "")
        context = {}
        utils.add_word(word, translation, email)
        return render(request, "add_word_res_page.html", context)
    else:
        add_word(request)


def find_word(request):
    return render(request, "find_word_page.html")


def send_word_translate(request):
    if request.method == "POST":
        cache.clear()
        search_type = request.POST.get("search_type")
        search_object = request.POST.get("search_object")
        context = {"search_type_word": (search_type == 'word'),
                   "search_object": search_object,
                   "results": utils.find_word(search_type, search_object)}
        if len(context["results"]) == 0:
            context["success"] = False
        else:
            context["success"] = True
        return render(request, "find_word_res_page.html", context)
    else:
        find_word(request)


def show_stats(request):
    stats = utils.get_words_stats()
    return render(request, "show_stats_page.html", stats)
