from django.shortcuts import get_object_or_404, _get_queryset
from pypdf import PdfReader
from rest_framework.pagination import PageNumberPagination
from users.models import User


def get_client_username(request):
    user = get_object_or_404(User, email=request.user.email)
    return user


def get_object_or_void(klass, *args, **kwargs):
    """
    Use get() to return an object, or raise an Http404 exception if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
    one object is found.
    """
    queryset = _get_queryset(klass)
    if not hasattr(queryset, "get"):
        klass__name = (
            klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        )
        raise ValueError(
            "First argument to get_object_or_404() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return


def parse_pdf(filename):
    data_ls = []
    count = 0

    reader = PdfReader(filename)
    pages = reader.pages
    for page in pages:
        count += 1
        data_ls.append({f"{count}": page.extract_text()})

    return data_ls


class BookAPIPagination(PageNumberPagination):
    page_size = 1
    max_page_size = 10000
    signal_start = None




