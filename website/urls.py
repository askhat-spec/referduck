from django.urls import path
from . import views

urlpatterns = [
    path("", views.CategoryView.as_view(), name='main'),
    path("show/<slug:slug>", views.PaperDetailView.as_view(), name='paper_detail'),
    path("category/<slug:cat_slug>/", views.PaperListView.as_view(), name='category'),
    path("search/", views.Search.as_view(), name='search')
]