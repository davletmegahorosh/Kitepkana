from django.shortcuts import get_object_or_404, _get_queryset
from pypdf import PdfReader
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from users.models import User
import re
from difflib import SequenceMatcher
from django.core.exceptions import (
    FieldDoesNotExist,
    ValidationError,
)
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import exceeds_maximum_length_ratio


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


def validate_star(value):
    if value == '' or value is None:
        raise ValidationError({"star": ["This field is required."]})
    try:
        if int(value):
            pass
    except ValueError:
        raise ValidationError('Value must be a numeric type')

    if int(value) > 5:
        raise ValidationError('value must be less than or equal to 5')
    if int(value) < 1:
        raise ValidationError('value must be equal')
    return value



class UserAttributeSimilarityValidator:
    """
    Validate that the password is sufficiently different from the user's
    attributes.

    If no specific attributes are provided, look at a sensible list of
    defaults. Attributes that don't exist are ignored. Comparison is made to
    not only the full attribute value, but also its components, so that, for
    example, a password is validated against either part of an email address,
    as well as the full address.
    """

    DEFAULT_USER_ATTRIBUTES = ("username", "first_name", "last_name")

    def __init__(self, user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0.7):
        self.user_attributes = user_attributes
        if max_similarity < 0.1:
            raise ValueError("max_similarity must be at least 0.1")
        self.max_similarity = max_similarity

    def validate(self, password, user=None):
        if not user:
            return

        password = password.lower()
        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_lower = value.lower()
            value_parts = re.split(r"\W+", value_lower) + [value_lower]
            for value_part in value_parts:
                if exceeds_maximum_length_ratio(
                    password, self.max_similarity, value_part
                ):
                    continue
                if (
                    SequenceMatcher(a=password, b=value_part).quick_ratio()
                    >= self.max_similarity
                ):
                    try:
                        verbose_name = str(
                            user._meta.get_field(attribute_name).verbose_name
                        )
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        _("The password is too similar to the %(verbose_name)s."),
                        code="password_too_similar",
                        params={"verbose_name": verbose_name},
                    )

    def get_help_text(self):
        return _(
            "Your password can’t be too similar to your other personal information."
        )

