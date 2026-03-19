from django.views import View
from django.shortcuts import render


# plain old view.
def home_page_view(request):
    return render(
        request,
        "web/home.html",
    )


# rewrite as class based view.
# add the url correctly as well.
class HomePageView(View):
    template_name = "web/home.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
        )
