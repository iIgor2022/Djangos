from django.shortcuts import render, reverse

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    "pizza": {
        "1, 2": 1,
    }
    # можете добавить свои рецепты ;)
}


def home_view(request):
    template_name = "calculator/home.html"
    pages = {
        "Главная страница": reverse("home"),

    }
    for key in DATA.keys():
        pages[key] = key
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def recepies(request, recepie_name):
    template_name = "calculator/index.html"
    count_ingridients = request.GET.get("servings")
    if count_ingridients is None:
        context = {"recipe": DATA.get(recepie_name)}
    else:
        ingridients = DATA.get(recepie_name)
        count_ingridients = int(count_ingridients)
        if ingridients is not None:
            ingridients = {key: value * count_ingridients for key, value in ingridients.items()}
            context = {"recipe": ingridients}


    return render(request, template_name, context)

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }
