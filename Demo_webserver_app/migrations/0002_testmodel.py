# Generated by Django 3.2.5 on 2021-07-11 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Demo_webserver_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TestField', models.IntegerField()),
            ],
        ),
    ]