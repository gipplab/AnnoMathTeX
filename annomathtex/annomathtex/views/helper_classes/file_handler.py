import json

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from jquery_unparam import jquery_unparam


class FileHandler:

    def __init__(self, request):
        self.items = {k: jquery_unparam(v) for (k, v) in request.POST.items()}
