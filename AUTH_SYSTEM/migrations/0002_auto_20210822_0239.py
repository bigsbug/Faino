# Generated by Django 3.2.6 on 2021-08-22 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AUTH_SYSTEM', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new_user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='new_user',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
    ]
