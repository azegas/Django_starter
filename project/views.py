from django.shortcuts import render
from django.views import View
from django.http import HttpResponse


class Index(View):
    def get(self, request):
        return render(request, "project/index.html")

    
def test(request):
    return HttpResponse('<h2>Test</h2>')
