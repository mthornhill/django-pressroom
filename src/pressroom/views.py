from datetime import datetime

from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView

from models import Section

class SectionListView(ListView):
    template_name = "pressroom/view_section.html"
    def get_queryset(self):
        self.section = get_object_or_404(Section, slug__iexact=self.kwargs['slug'])
        return self.section.articles.filter(publish=True, pub_date__lte=datetime.now())
