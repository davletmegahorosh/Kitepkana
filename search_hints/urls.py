from search_hints.views import BookSearchHintsView
from django.urls import path


urlpatterns = [
    path('search_hints/', BookSearchHintsView.as_view(), name='search-hints')
]

