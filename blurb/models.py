import textwrap

from django.db import models


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