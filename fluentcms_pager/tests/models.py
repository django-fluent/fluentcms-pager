from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from fluent_contents.models import PlaceholderField


@python_2_unicode_compatible
class ExamplePage(models.Model):
    slug = models.SlugField()
    position = models.IntegerField()

    content = PlaceholderField(slot='content')

    class Meta:
        ordering = ('position',)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return '/foo/{0}/'.format(self.slug)

    def get_previous_sibling(self):
        # Simulate API of django-mptt
        try:
            return ExamplePage.objects.filter(position__lt=self.position).order_by('-position')[0]
        except IndexError:
            return None

    def get_next_sibling(self):
        try:
            return ExamplePage.objects.filter(position__gt=self.position).order_by('position')[0]
        except IndexError:
            return None
