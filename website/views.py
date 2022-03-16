from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.list import MultipleObjectMixin
# from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank, SearchHeadline
from django.conf import settings

from .models import Paper, Category


class CategoryView(ListView):
    model = Category
    queryset = Category.objects.all()
    template_name = 'website/index.html'


class PaperListView(ListView):
    model = Paper
    template_name = 'website/papers_list.html'
    allow_empty = False
    paginate_by = 20

    def get_queryset(self):
        return Paper.objects.filter(category__url=self.kwargs['cat_slug'], visibility=True)


class PaperDetailView(DetailView, MultipleObjectMixin):
    model = Paper
    slug_field = 'url'
    context_object_name = 'paper'
    template_name = 'website/paper_detail.html'
    paginate_by = 80
    
    def get_context_data(self, **kwargs):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        object_list = Paper.objects.get(url=slug).content.split('`')
        context = super(PaperDetailView, self).get_context_data(object_list=object_list, **kwargs)
        return context


class Search(ListView):
    paginate_by = 20
    template_name = 'website/search_results.html'
    allow_empty = False
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        if not settings.DEBUG:
            vector = SearchVector('title', 'content')
            query = SearchQuery(q)
            search_headline = SearchHeadline('content', query)
            object_list = Paper.objects.annotate(rank=SearchRank(vector, query)).annotate(headline=search_headline).filter(rank__gte=0.001).order_by('-rank')
        else:
            object_list = Paper.objects.filter(title__icontains=q)
        return object_list

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context