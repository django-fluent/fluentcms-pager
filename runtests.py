#!/usr/bin/env python
import sys
import django
from django.conf import settings, global_settings as default_settings
from django.core.management import execute_from_command_line

if not settings.configured:
    settings.configure(
        DATABASES = {
            'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:',},
        },
        SITE_ID = 1,
        INSTALLED_APPS = (
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'django.contrib.sites',
            'fluent_contents',
            'fluentcms_pager',
            'fluentcms_pager.tests',
        ),
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': (),
                'OPTIONS': {
                    'loaders': (
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                    ),
                    'context_processors': (
                        'django.template.context_processors.debug',
                        'django.template.context_processors.i18n',
                        'django.template.context_processors.media',
                        'django.template.context_processors.request',
                        'django.template.context_processors.static',
                        'django.contrib.auth.context_processors.auth',
                    ),
                },
            },
        ],
        MIDDLEWARE = (),
        FLUENT_CONTENTS_CACHE_OUTPUT = False,
        TEST_RUNNER = 'django.test.runner.DiscoverRunner',
    )

DEFAULT_TEST_APPS = [
    'fluentcms_pager',
]


def runtests():
    other_args = list(filter(lambda arg: arg.startswith('-'), sys.argv[1:]))
    test_apps = list(filter(lambda arg: not arg.startswith('-'), sys.argv[1:])) or DEFAULT_TEST_APPS
    argv = sys.argv[:1] + ['test', '--traceback'] + other_args + test_apps
    execute_from_command_line(argv)

if __name__ == '__main__':
    runtests()
