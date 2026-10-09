from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404

SERVICES = [
    {"slug": "audit-sayta", "title": "Аудит сайта", "price": 7900, "days": 3},
    {"slug": "logo-design", "title": "Дизайн логотипа", "price": 12000, "days": 5},
]


def home(request):
    return HttpResponse("<h1>DigiStore — магазин электронных услуг</h1>")


def service_list(request):
    services = SERVICES

    # ?max_price=10000 - the parameter may be missing or garbage, so validate it
    raw = request.GET.get("max_price")
    if raw and raw.isdigit():
        limit = int(raw)
        services = [s for s in services if s["price"] <= limit]

    # Build the HTML as a string for now
    items = "".join(
        f"<li>{s['title']} — {s['price']} ₽, {s['days']} дн.</li>"
        for s in services
    )
    return HttpResponse(f"<h1>Услуги</h1><ul>{items}</ul>")


def service_detail(request, slug):
    # Look the service up by slug; no match means a 404 page
    for item in SERVICES:
        if item["slug"] == slug:
            return HttpResponse(
                f"<h1>{item['title']}</h1>"
                f"<p>Цена: {item['price']} ₽</p>"
                f"<p>Срок: {item['days']} дн.</p>"
            )
    raise Http404("Услуга не найдена")


def category_detail(request, slug):
    # For now just show the category slug taken from the URL
    return HttpResponse(f"Категория: {slug}")