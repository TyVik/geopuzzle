# Generated by Django 2.2.8 on 2020-01-06 04:05

from django.db import migrations
import django_enumfield.db.fields
import maps.constants


class Migration(migrations.Migration):

    dependencies = [
        ('puzzle', '0010_auto_20181121_0753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puzzle',
            name='zoom',
            field=django_enumfield.db.fields.EnumField(default=6, enum=maps.constants.Zoom),
        ),
    ]
