from django.template import Template, Context
from django.test import TestCase, override_settings, RequestFactory
from django.utils.html import strip_tags
from fluent_contents.models import Placeholder

from fluentcms_pager.models import PagerItem
from .models import ExamplePage


class PagerTests(TestCase):
    """
    Testing pagers
    """

    def test_example_page_model(self):
        """
        Make sure our test model also works as expected
        """
        page1 = ExamplePage.objects.create(slug='page1', position=1)
        page2 = ExamplePage.objects.create(slug='page2', position=2)
        page3 = ExamplePage.objects.create(slug='page3', position=3)

        self.assertEqual(page1.get_previous_sibling(), None)
        self.assertEqual(page1.get_next_sibling(), page2)
        self.assertEqual(page2.get_previous_sibling(), page1)
        self.assertEqual(page2.get_next_sibling(), page3)
        self.assertEqual(page3.get_previous_sibling(), page2)
        self.assertEqual(page3.get_next_sibling(), None)

    @classmethod
    def create_page(cls, slug, position, **pager_kwargs):
        """
        Factory to create an page
        """
        page = ExamplePage.objects.create(slug=slug, position=position)
        placeholder = Placeholder.objects.create_for_object(page, slot='content')
        PagerItem.objects.create_for_placeholder(placeholder, **pager_kwargs)
        return page

    @override_settings(FLUENT_CONTENTS_CACHE_OUTPUT=False)  # in runtests.py disabled
    def test_default_pager(self):
        """
        Default pager rendering
        """
        page1 = self.create_page(slug='page1', position=1)
        page2 = self.create_page(slug='page2', position=2)
        page3 = self.create_page(slug='page3', position=3)

        template = Template('{% load fluent_contents_tags %}{% page_placeholder "content" %}')
        request = RequestFactory().get("/", HTTP_HOST='example.org')

        # Standard pagers
        html1 = template.render(Context({'page': page1, 'request': request}))
        html2 = template.render(Context({'page': page2, 'request': request}))
        html3 = template.render(Context({'page': page3, 'request': request}))

        self.assertEqual(strip_tags(html1).strip(), 'page2 &rarr;')
        self.assertEqual(strip_tags(html2).strip(), '&larr; page1\n    page3 &rarr;')
        self.assertEqual(strip_tags(html3).strip(), '&larr; page2')

        self.assertTrue('<li class="previous"><a href="/foo/page1/">' in html2)
        self.assertTrue('<li class="next"><a href="/foo/page3/">' in html2)

    @override_settings(FLUENT_CONTENTS_CACHE_OUTPUT=False)  # in runtests.py disabled
    def test_no_arrows(self):
        """
        Pager without arrows
        """
        page1 = self.create_page(slug='page1', position=1, show_arrows=False)
        page2 = self.create_page(slug='page2', position=2, show_arrows=False)
        page3 = self.create_page(slug='page3', position=3, show_arrows=False)

        template = Template('{% load fluent_contents_tags %}{% page_placeholder "content" %}')
        request = RequestFactory().get("/", HTTP_HOST='example.org')

        html1 = template.render(Context({'page': page1, 'request': request}))
        html2 = template.render(Context({'page': page2, 'request': request}))
        html3 = template.render(Context({'page': page3, 'request': request}))

        self.assertEqual(strip_tags(html1).strip(), 'page2')
        self.assertEqual(strip_tags(html2).strip(), 'page1\n    page3')
        self.assertEqual(strip_tags(html3).strip(), 'page2')

    @override_settings(FLUENT_CONTENTS_CACHE_OUTPUT=False)  # in runtests.py disabled
    def test_other_titles(self):
        """
        Pager with custom title
        """
        page1 = self.create_page(slug='page1', position=1, previous_title='N/A', next_title='PAGE2')
        page2 = self.create_page(slug='page2', position=2, previous_title='PAGE1', next_title='PAGE3')
        page3 = self.create_page(slug='page3', position=3, previous_title='PAGE2', next_title='N/A')

        template = Template('{% load fluent_contents_tags %}{% page_placeholder "content" %}')
        request = RequestFactory().get("/", HTTP_HOST='example.org')

        html1 = template.render(Context({'page': page1, 'request': request}))
        html2 = template.render(Context({'page': page2, 'request': request}))
        html3 = template.render(Context({'page': page3, 'request': request}))

        self.assertEqual(strip_tags(html1).strip(), 'PAGE2 &rarr;')
        self.assertEqual(strip_tags(html2).strip(), '&larr; PAGE1\n    PAGE3 &rarr;')
        self.assertEqual(strip_tags(html3).strip(), '&larr; PAGE2')

    def test_other_urls(self):
        """
        Pager with custom URLs
        """
        page1 = self.create_page(slug='page1', position=1, previous_url='/FOO/NA/', next_url="/FOO/PAGE2/")
        page2 = self.create_page(slug='page2', position=2, previous_url='/FOO/PAGE1/', next_url="/FOO/PAGE3/")
        page3 = self.create_page(slug='page3', position=3, previous_url='/FOO/PAGE2/', next_url="/FOO/NA/")

        template = Template('{% load fluent_contents_tags %}{% page_placeholder "content" %}')
        request = RequestFactory().get("/", HTTP_HOST='example.org')

        html1 = template.render(Context({'page': page1, 'request': request}))
        html2 = template.render(Context({'page': page2, 'request': request}))
        html3 = template.render(Context({'page': page3, 'request': request}))

        self.assertTrue('<li class="previous"><a href="/FOO/NA/">' in html1)
        self.assertTrue('<li class="next"><a href="/FOO/PAGE2/">' in html1)
        self.assertTrue('<li class="previous"><a href="/FOO/PAGE1/">' in html2)
        self.assertTrue('<li class="next"><a href="/FOO/PAGE3/">' in html2)
        self.assertTrue('<li class="previous"><a href="/FOO/PAGE2/">' in html3)
        self.assertTrue('<li class="next"><a href="/FOO/NA/">' in html3)
