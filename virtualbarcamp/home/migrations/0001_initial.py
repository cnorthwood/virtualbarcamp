# Generated by Django 3.0.6 on 2020-05-12 21:17

from django.db import migrations, models


def create_global_settings(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    apps.get_model("home", "GlobalSettings").objects.using(db_alias).create()


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="GlobalSettings",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("allow_registration", models.BooleanField(default=False)),
            ],
        ),
        migrations.RunPython(create_global_settings),
    ]
