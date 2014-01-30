# -*- coding: utf-8 -*-

import sys

from django.db.models.signals import post_migrate
from django.db import connection
from django.dispatch import receiver

def setup_custom_indexes():
    print("Setup custom indexes...", file=sys.stderr)

    sql = "select indexname from pg_indexes where indexname = %s;"
    sql_params = ["issues_unpickle_tags_index"]

    index_exists = False

    with connection.cursor() as c:
        c.execute(sql, sql_params)
        index_exists = bool(c.fetchone())

    if index_exists:
        return

    sql_index = ("CREATE INDEX issues_unpickle_tags_index ON "
                 "issues_issue USING btree (unpickle(tags));")
    with connection.cursor() as c:
        c.execute(sql_index)


def setup_plpython():
    print("Setup plpythonu postgresql procedural language...", file=sys.stderr)

    sql = "select * from pg_language where lanname = %s;"
    sql_params = ["plpythonu"]

    lang_exists = False

    with connection.cursor() as c:
        c.execute(sql, sql_params)
        lang_exists = bool(c.fetchone())

    if lang_exists:
        return

    with connection.cursor() as c:
        c.execute("CREATE LANGUAGE plpythonu;")


def setup_stored_functions():
    print("Setup plpythonu postgresql functions...", file=sys.stderr)
    sql = ["CREATE OR REPLACE FUNCTION unpickle (data text)",
           "    RETURNS text[]",
           "AS $$",
           "    import base64",
           "    import pickle",
           "    return pickle.loads(base64.b64decode(data))",
           "$$ LANGUAGE plpythonu IMMUTABLE;"]

    with connection.cursor() as c:
        c.execute("\n".join(sql))


@receiver(post_migrate)
def on_post_migrate(sender, **kwargs):
    if sender.name == "taiga":
        setup_plpython()
        setup_stored_functions()
        setup_custom_indexes()
