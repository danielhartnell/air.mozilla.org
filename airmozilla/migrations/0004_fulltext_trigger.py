# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-18 15:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('airmozilla', '0003_event_fulltext'),
    ]

    operations = [
        migrations.RunSQL(
            """
            -- 'simple' does not do stemming
            CREATE TEXT SEARCH CONFIGURATION simple_unaccent (COPY = simple);
            ALTER TEXT SEARCH CONFIGURATION simple_unaccent
                ALTER MAPPING FOR hword, hword_part, word
                WITH unaccent;

            CREATE FUNCTION update_event_fulltext() RETURNS trigger AS $$
            begin
                new.fulltext :=
                    setweight(to_tsvector('public.english_unaccent', new.title), 'A') ||
                    setweight(to_tsvector('public.english_unaccent', new.description), 'B') ||
                    setweight(to_tsvector('public.simple_unaccent', new.title), 'A') ||
                    setweight(to_tsvector('public.simple_unaccent', new.description), 'B');
                return new;
            end
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER update_event_fulltext BEFORE INSERT OR UPDATE
                ON airmozilla_event FOR EACH ROW EXECUTE PROCEDURE
                update_event_fulltext();
            """,
            """
            DROP FUNCTION update_event_fulltext();
            DROP TEXT SEARCH CONFIGURATION simple_unaccent;
            """
        ),
    ]
