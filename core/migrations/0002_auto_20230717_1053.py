# Generated by Django 4.2.3 on 2023-07-17 10:53

from django.db import migrations

GLOBAL = 1
EXTERNAL_REQUEST = 2
PETITIONS = 3


def set_timers(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Timers = apps.get_model("core", "Timers")
    Timers.objects.create(seconds=2, timer_type=GLOBAL)
    Timers.objects.create(seconds=2, timer_type=EXTERNAL_REQUEST)
    Timers.objects.create(seconds=2, timer_type=PETITIONS)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [migrations.RunPython(set_timers), ]
