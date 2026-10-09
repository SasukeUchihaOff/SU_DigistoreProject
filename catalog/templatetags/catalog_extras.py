from django import template
from catalog.views import SERVICES

register = template.Library()


@register.filter
def rubles(value):
    """7900 -> '7 900 ₽'"""
    try:
        return f"{int(value):,} ₽".replace(",", " ")
    except (TypeError, ValueError):
        return value


@register.filter
def days_ru(value):
    """1 -> '1 день', 3 -> '3 дня', 5 -> '5 дней'"""
    try:
        n = int(value)
    except (TypeError, ValueError):
        return value
    # 11-14 always take the "many" form
    if 11 <= n % 100 <= 14:
        word = "дней"
    elif n % 10 == 1:
        word = "день"
    elif 2 <= n % 10 <= 4:
        word = "дня"
    else:
        word = "дней"
    return f"{n} {word}"


@register.inclusion_tag("catalog/_popular.html")
def popular_services(count=3):
    # For now "popular" means the first `count` services of the list
    return {"services": SERVICES[:count]}