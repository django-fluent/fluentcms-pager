fluentcms-pager
===============

.. toctree::
   :maxdepth: 2

Displaying a Bootstrap 3 pager_ in a page

Features:

* Arrows
* Previous/next links
* Automatic title retrieval


Installation
============

First install the module, preferably in a virtual environment. It can be installed from PyPI:

.. code-block:: bash

    pip install fluentcms-pager

First make sure the project is configured for django-fluent-contents_.

Then add the following settings:

.. code-block:: python

    INSTALLED_APPS += (
        'fluentcms_pager',
    )

The database tables can be created afterwards:

.. code-block:: bash

    ./manage.py migrate


Frontend styling
================

The pager is renderd with the HTML that Bootstrap prescribes:

.. code-block:: html+django

    <ul class="pager">
      <li class="previous"><a href="#"><span aria-hidden="true">&larr;</span> Older</a></li>
      <li class="next"><a href="#">Newer <span aria-hidden="true">&rarr;</span></a></li>
    </ul>

The standard Bootstrap 3 CSS will provide a reasonable styling for this,
which can either be overwritten, or replaced in your own CSS files.


Contributing
------------

If you like this module, forked it, or would like to improve it, please let us know!
Pull requests are welcome too. :-)

.. _django-fluent-contents: https://github.com/edoburu/django-fluent-contents
.. _pager: http://getbootstrap.com/components/#pagination-pager
