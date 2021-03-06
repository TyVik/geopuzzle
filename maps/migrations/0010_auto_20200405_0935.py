# Generated by Django 2.2.12 on 2020-04-05 09:35
from django.contrib.postgres.operations import TrigramExtension

import common.db
from django.db import migrations
import maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0009_auto_20200106_0405'),
    ]

    operations = [
        TrigramExtension(),
        migrations.AlterField(
            model_name='region',
            name='wikidata_id',
            field=maps.fields.ExternalIdField(db_index=True, max_length=20, null=True),
        ),
        migrations.AddIndex(
            model_name='regiontranslation',
            index=common.db.GinIndexTrgrm(fields=['name'], name='maps_region_name_edae1f_gin'),
        ),
    ]
