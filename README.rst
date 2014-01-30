Taiga Backend
=================

.. image:: http://kaleidos.net/static/img/badge.png
    :target: http://kaleidos.net/community/taiga/

.. image:: https://travis-ci.org/kaleidos/taiga-back.png?branch=master
    :target: https://travis-ci.org/kaleidos/taiga-back

.. image:: https://coveralls.io/repos/kaleidos/taiga-back/badge.png?branch=master
    :target: https://coveralls.io/r/kaleidos/taiga-back?branch=master

.. image:: https://d2weczhvl823v0.cloudfront.net/kaleidos/taiga-back/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free


Setup development environment
-----------------------------

Just execute these commands in your virtualenv(wrapper):

.. code-block:: console

    pip install -r requirements.txt
    python manage.py migrate --noinput
    python manage.py loaddata initial_user
    python manage.py sample_data
    python manage.py createinitialrevisions


Note: taiga only runs with python 3.3+.

Note: Initial auth data: admin/123123


Polyfills
---------

Django-Rest Framework by default returns 403 for not authenticated requests and permission denied
requests. The file ``taiga/base/monkey.py`` contains a temporary fix for this bug.

This patch is applied when the module ``base.models`` it's loaded. Once it's solved on django rest
framework, this patch can be removed.
