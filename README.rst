django-mediacracy
=================

Ruled by the mass media! This integrates ``django-textify``, ``django-massmedia``,
and ``django-markitup``. To use, add

    mediacracy
    textify
    massmedia
    markitup

to your ``INSTALLED_APPS``. Be sure to include the following settings:

    TEXTIFY_SETTINGS = {
        'WIDGET': 'mediacracy.widgets.TextifyMarkitupAdminWidget'
    }