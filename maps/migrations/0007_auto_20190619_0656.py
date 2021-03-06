# Generated by Django 2.2.2 on 2019-06-19 06:56

from django.db import migrations


def migrate_tags(apps, schema):
    Tag = apps.get_model('maps', 'tag')
    for tag_id in Tag.objects.values_list('id', flat=True):
        tag = Tag.objects.get(pk=tag_id)
        tag_ru = Tag.objects.create(name=tag.name_ru)
        tag_en = Tag.objects.create(name=tag.name_en)
        for puzzle in tag.puzzle_set.all():
            puzzle.tags.add(tag_ru)
            puzzle.tags.add(tag_en)
        tag.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0006_tag_name'),
    ]

    operations = [
        migrations.RunPython(migrate_tags),
    ]
