# Generated by Django 2.2.2 on 2019-06-19 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0005_auto_20181104_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
