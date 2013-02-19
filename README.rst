django-mediacracy
=================

Ruled by the mass media! This integrates ``django-textify``, ``django-massmedia``,
and ``django-markitup``. To use, set

    INSTALLED_APPS = {
        ...,
        'mediacracy',
        'textify',
        'massmedia',
        'markitup',
        ...,
    }

in your ``SETTINGS``. Be sure to keep ``mediacracy`` above ``massmedia``.
And add ``(r'^mediacracy/', include('mediacracy.urls')), url(r'^browse/', 'massmedia.views.browse', name="fb_browse"),`` to your urls. 

