# Generated by Django 3.2.22 on 2024-01-01 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_first_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to='avatars', verbose_name='Avatar'),
        ),
    ]
