from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q

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
    paginate_by = 15

    def get_queryset(self):
        return Paper.objects.filter(category__url=self.kwargs['cat_slug'], visibility=True)


class PaperDetailView(DetailView):
    model = Paper
    slug_field = 'url'
    context_object_name = 'paper'
    template_name = 'website/paper_detail.html'


class Search(ListView):
    paginate_by = 15
    template_name = 'website/search_results.html'
    allow_empty = False
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Paper.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        return object_list

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context