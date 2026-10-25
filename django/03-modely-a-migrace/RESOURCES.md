# 03 — Modely a migrace — zdroje

## V tomhle repu

- [`../docs/MODELS_AND_FIELDS.md`](../docs/MODELS_AND_FIELDS.md) — pole, volby, `Meta`, validace
- [`../docs/MIGRATIONS.md`](../docs/MIGRATIONS.md) — příkazy, workflow, situace z praxe
- [`../docs/ORM_BASICS.md`](../docs/ORM_BASICS.md) — CRUD, shell, lookupy
- [`../docs/DATABASE.md`](../docs/DATABASE.md) — SQLite, PyCharm Database, fixtures, PostgreSQL

## Oficiální dokumentace

- [Models](https://docs.djangoproject.com/en/6.1/topics/db/models/) —
  úvod do modelů, `Meta`, metody
- [Model field reference](https://docs.djangoproject.com/en/6.1/ref/models/fields/)
  — všechna pole a jejich volby (`null`, `blank`, `choices`, `default`…)
- [Constraints reference](https://docs.djangoproject.com/en/6.1/ref/models/constraints/)
  — `UniqueConstraint`, `CheckConstraint`
- [Model instance reference](https://docs.djangoproject.com/en/6.1/ref/models/instances/)
  — `save()`, `delete()`, `full_clean()`, `refresh_from_db()`
- [Migrations](https://docs.djangoproject.com/en/6.1/topics/migrations/)
  — jak migrace fungují, workflow, datové migrace
- [Making queries](https://docs.djangoproject.com/en/6.1/topics/db/queries/)
  — CRUD a filtrování
- [QuerySet API reference](https://docs.djangoproject.com/en/6.1/ref/models/querysets/)
  — všechny metody a lookupy
- [`django-admin` příkazy](https://docs.djangoproject.com/en/6.1/ref/django-admin/)
  — `makemigrations`, `migrate`, `shell`, `dumpdata`, `loaddata`
- [Databases — SQLite notes](https://docs.djangoproject.com/en/6.1/ref/databases/#sqlite-notes)
  — omezení SQLite

## Pro srovnání z FE

- [Prisma — Data model](https://www.prisma.io/docs/orm/prisma-schema/data-model/models)
  a [Prisma Migrate](https://www.prisma.io/docs/orm/prisma-migrate) —
  stejné myšlenky v TS světě (schema → migrace → klient)
