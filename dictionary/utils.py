from dbconnect.models import Dictionary
from datetime import date, timedelta


def get_words_for_table():
    entries = []
    for i, item in enumerate(Dictionary.objects.all()):
        entries.append([i + 1, item.word, item.translation])
    return entries


def add_word(word, translation, email):
    entry = Dictionary(word=word,
                       translation=translation,
                       added_date=date.today(),
                       added_email=email)
    entry.save()


def get_words_stats():
    entries = Dictionary.objects.all()

    words_all = len(entries)

    today = date.today()
    words_day = len(Dictionary.objects.filter(added_date=today))

    last_week = [today]
    for i in range(6):
        last_week.append(last_week[i] + timedelta(days=-1))
    words_week = sum([len(Dictionary.objects.filter(added_date=day)) for day in last_week])

    last_month = [today]
    for i in range(30):
        last_month.append(last_month[i] + timedelta(days=-1))
    words_month = sum([len(Dictionary.objects.filter(added_date=day)) for day in last_month])

    unsorted_users = {}
    for entry in entries:
        if entry.added_email not in unsorted_users.keys():
            unsorted_users[entry.added_email] = 1
        else:
            unsorted_users[entry.added_email] += 1
    sorted_keys = sorted(unsorted_users, key=unsorted_users.get, reverse=True)
    users_activity = []
    i = 1
    for user in sorted_keys:
        users_activity.append([i, user, unsorted_users[user]])
        i += 1

    stats = {
        "words_all": words_all,
        "words_day": words_day,
        "words_week": words_week,
        "words_month": words_month,
        "users_activity": users_activity
    }
    return stats


def find_word(search_type, search_object):
    if search_type == 'word':
        return [entry.translation for entry in Dictionary.objects.filter(word=search_object)]
    elif search_type == 'translation':
        return [entry.word for entry in Dictionary.objects.filter(translation=search_object)]
