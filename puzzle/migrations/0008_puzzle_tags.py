# Generated by Django 2.1.2 on 2018-11-04 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0005_auto_20181104_1942'),
        ('puzzle', '0007_auto_20180509_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='puzzle',
            name='tags',
            field=models.ManyToManyField(to='maps.Tag'),
        ),
    ]
