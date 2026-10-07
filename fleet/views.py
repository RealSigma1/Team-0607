from django.db import DatabaseError, connection
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .models import Car


@require_GET
def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            if cursor.fetchone() != (1,):
                raise DatabaseError("Unexpected database response")
    except DatabaseError:
        return JsonResponse({"status": "unavailable"}, status=503)
    return JsonResponse({"status": "ok", "database": "ok"})


@require_GET
def catalog(request):
    try:
        cars = list(Car.objects.order_by("inventory_code")[:100])
    except DatabaseError:
        return JsonResponse({"status": "unavailable"}, status=503)
    return render(request, "fleet/catalog.html", {"cars": cars})
