# Generated by Django 2.0.3 on 2018-06-05 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20180203_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_subscribed',
            field=models.BooleanField(default=True, verbose_name='Subscribed on news'),
            preserve_default=False,
        ),
    ]
