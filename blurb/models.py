import textwrap

from django.db import models
from django.contrib import admin


class Blurb(models.Model):
    identifier = models.CharField(max_length=512, unique=True)
    # A null value indicates that the content has not been set.
    # An empty value would indicate that the blurb is intentionally empty.
    content = models.TextField('content', 'content', blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['identifier']),
        ]

    def empty(self):
        return self.content == ''

    def __str__(self):
        content = self.content
        if content == None:
            content = '<PLEASE FILL IN THIS BLURB>'
        elif content == '':
            content = '<EMPTY>'
        content = textwrap.shorten(content, width=80, placeholder='...')
        return '[{}] {}'.format(self.identifier, content)


class BlurbFilledFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Fill Status'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'filled'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (('true', 'Filled'), ('false', 'Not Filled'))

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'true':
            return queryset.filter(content__isnull=False)
        if self.value() == 'false':
            return queryset.filter(content__isnull=True)


@admin.register(Blurb)
class BlurbAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'content', 'filled')
    list_filter = (BlurbFilledFilter, )
    ordering = ('identifier', )

    def filled(self, blurb):
        return blurb.content is not None

    filled.boolean = True