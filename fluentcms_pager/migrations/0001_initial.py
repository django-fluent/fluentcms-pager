# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import fluent_contents.extensions


class Migration(migrations.Migration):

    dependencies = [
        ('fluent_contents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PagerItem',
            fields=[
                ('contentitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem')),
                ('previous_title', models.CharField(max_length=200, null=True, verbose_name='Title previous link', blank=True)),
                ('previous_url', fluent_contents.extensions.PluginUrlField(max_length=300, null=True, verbose_name='URL previous link', blank=True)),
                ('next_title', models.CharField(max_length=200, null=True, verbose_name='Title next link', blank=True)),
                ('next_url', fluent_contents.extensions.PluginUrlField(max_length=300, null=True, verbose_name='URL next link', blank=True)),
                ('show_arrows', models.BooleanField(default=True, verbose_name='Show arrows')),
                ('show_previous', models.BooleanField(default=True, verbose_name='Show previous link')),
                ('show_next', models.BooleanField(default=True, verbose_name='Show next link')),
            ],
            options={
                'db_table': 'contentitem_fluentcms_pager_pageritem',
                'verbose_name': 'Pager',
                'verbose_name_plural': 'Pagers',
            },
            bases=('fluent_contents.contentitem',),
        ),
    ]
