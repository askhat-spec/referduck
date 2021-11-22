from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import Paper, Category


class CategoryView(ListView):
    model = Category
    queryset = Category.objects.all()
    template_name = 'website/index.html'


class PaperListView(ListView):
    model = Paper
    queryset = Paper.objects.filter(visibility=True)
    template_name = 'website/papers_list.html'
    allow_empty = False
    paginate_by = 20

    def get_queryset(self):
        return Paper.objects.filter(category__url=self.kwargs['cat_slug'], visibility=True)


class PaperDetailView(DetailView):
    model = Paper
    slug_field = 'url'
    context_object_name = 'paper'
    template_name = 'website/paper_detail.html'