"""A module for project views. Currently have only index."""

from django.shortcuts import render
from django.views import View


class Index(View):
    """
    Renders an index page.
    """

    def get(self, request):
        """
        What happens when GET method knocks on this view's door.
        """

        return render(request, "project/index.html")
