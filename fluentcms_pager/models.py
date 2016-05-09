from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible, force_text
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from fluent_contents.extensions import PluginUrlField
from fluent_contents.models import ContentItem

USE_ANY_URL_FIELD = 'any_urlfield' in settings.INSTALLED_APPS


@python_2_unicode_compatible
class PagerItem(ContentItem):
    """
    Pager item, to show a previous/next page.
    The pages are auto determined, but can be overwritten
    """
    show_arrows = models.BooleanField(_("Show arrows"), default=True, blank=True)
    show_previous = models.BooleanField(_("Show previous link"), default=True, blank=True)
    show_next = models.BooleanField(_("Show next link"), default=True, blank=True)
    previous_title = models.CharField(_("Title previous link"), max_length=200, blank=True, null=True)
    previous_url = PluginUrlField(_("URL previous link"), blank=True, null=True)
    next_title = models.CharField(_("Title next link"), max_length=200, blank=True, null=True)
    next_url = PluginUrlField(_("URL next link"), blank=True, null=True)

    class Meta:
        verbose_name = _("Pager")
        verbose_name_plural = _("Pagers")

    def __str__(self):
        return u"{0} / {1}".format(self.previous_title, self.next_title)

    def get_previous_url(self):
        if self.previous_url:
            return force_text(self.previous_url)
        else:
            page = self.previous_parent_sibling
            return page.get_absolute_url() if page is not None else None

    def get_previous_title(self):
        if self.previous_title:
            return self.previous_title

        if USE_ANY_URL_FIELD and self.previous_url and self.previous_url.url_type.has_id_value:
            page = self.previous_url.get_object()
        else:
            page = self.previous_parent_sibling

        return force_text(page) if page is not None else _("Previous")

    def get_next_url(self):
        if self.next_url:
            return force_text(self.next_url)
        else:
            page = self.next_parent_sibling
            return page.get_absolute_url() if page is not None else None

    def get_next_title(self):
        if self.next_title:
            return self.next_title

        if USE_ANY_URL_FIELD and self.next_url and self.next_url.url_type.has_id_value:
            page = self.next_url.get_object()
        else:
            page = self.next_parent_sibling

        return force_text(page) if page is not None else _("Next")

    @cached_property
    def previous_parent_sibling(self):
        return self.parent.get_previous_sibling()

    @cached_property
    def next_parent_sibling(self):
        return self.parent.get_next_sibling()
