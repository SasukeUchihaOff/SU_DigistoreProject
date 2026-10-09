from django.http import HttpResponse


# Stubs: real logic comes in chapter 13
def order_list(request):
    return HttpResponse("My orders")


def order_create(request):
    return HttpResponse("Create order")


def order_detail(request, pk):
    return HttpResponse(f"Order {pk}")


def order_download(request, pk, item_id):
    return HttpResponse(f"Download item {item_id} of order {pk}")