import textwrap

from django.db import models


class Blurb(models.Model):
    page = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    # A null value indicates that the content has not been set.
    # An empty value would indicate that the blurb is intentionally empty.
    content = models.TextField('content', 'content', blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['page', 'name']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['page', 'name'],
                                    name='unique_identifier')
        ]

    def empty(self):
        return self.content == ''

    def get_identifier(self):
        return '{}:{}'.format(this.page, this.name)

    def __str__(self):
        content = self.content
        if content == None:
            content = '<PLEASE FILL IN THIS BLURB>'
        elif content == '':
            content = '<EMPTY>'
        content = textwrap.shorten(content, width=80, placeholder='...')
        return '[{}:{}] {}'.format(self.page, self.name, content)