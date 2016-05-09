"""
Definition of the plugin.
"""
from django.utils.translation import ugettext_lazy as _
from fluent_contents.extensions import ContentPlugin, plugin_pool
from .models import PagerItem


@plugin_pool.register
class PagerPlugin(ContentPlugin):
    """
    CMS plugin for previous/next navigation element.
    """
    category = _("Navigation")
    model = PagerItem
    render_template = "fluentcms_pager/pager.html"
    fieldsets = (
        (_("Previous link"), {
            'fields': ('show_previous', 'previous_title', 'previous_url'),
        }),
        (_("Next link"), {
            'fields': ('show_next', 'next_title', 'next_url'),
        }),
        (None, {
            'fields': ('show_arrows',),
        }),
    )

    class Media:
        js = (
            'admin/fluentcms_pager/pageradmin.js',
        )

    def get_context(self, request, instance, **kwargs):
        context = super(PagerPlugin, self).get_context(request, instance, **kwargs)
        show_next = instance.show_next
        show_previous = instance.show_previous
        context.update({
            'show_arrows': instance.show_arrows,
            'next_url': instance.get_next_url() if show_next else None,
            'next_title': instance.get_next_title() if show_next else None,
            'previous_url': instance.get_previous_url() if show_previous else None,
            'previous_title': instance.get_previous_title() if show_previous else None,
        })
        return context
