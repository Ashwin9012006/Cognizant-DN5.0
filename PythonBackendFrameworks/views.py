from django.http import HttpResponse

def hello_view(request):
    return HttpResponse(
        "Vehicle Service Management API is running"
    )