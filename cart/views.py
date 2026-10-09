from django.http import HttpResponse


# Stubs: real logic comes in chapter 12
def cart_detail(request):
    return HttpResponse("Cart")


def cart_add(request, service_id):
    return HttpResponse(f"Add service {service_id}")


def cart_remove(request, service_id):
    return HttpResponse(f"Remove service {service_id}")


def cart_clear(request):
    return HttpResponse("Clear cart")