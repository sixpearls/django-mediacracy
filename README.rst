django-mediacracy
=================

Ruled by the mass media! This integrates ``django-textify``, ``django-massmedia``,
and ``django-markitup``. To use, set ::

    INSTALLED_APPS = {
        ...,
        'mediacracy',
        'textify',
        'massmedia',
        'markitup',
        ...,
    }

in your ``SETTINGS``. Be sure to keep ``mediacracy`` above ``massmedia``. Add ::

    (r'^mediacracy/', include('mediacracy.urls')), 
    url(r'^browse/', 'massmedia.views.browse', name="fb_browse"),

to your ``URLconf``. If you have already built the ``massmedia`` SQL tables, use South to migrate them:

    $ ./manage.py migrate mediacracy
