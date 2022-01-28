import os

from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings


class ReactAppView(View):
    def get(self, request):
        with open(
            os.path.join(settings.BASE_DIR, "frontend", "index.html")
        ) as file:
            return HttpResponse(file.read())
