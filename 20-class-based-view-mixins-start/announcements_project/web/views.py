from django.shortcuts import render

# Create your views here.
from django.views import View
from django.shortcuts import render

class HomePageView(View):
    template_name = 'web/home.html'

    def get(self, request):
        return render(request, self.template_name)

