# Generated by Django 3.2.6 on 2022-01-31 19:42

import WEB_SERVER.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('AUTH_SYSTEM', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=36)),
                ('ip', models.CharField(blank=True, max_length=64)),
                ('password', models.CharField(blank=True, max_length=62)),
                ('mac', models.CharField(blank=True, max_length=17)),
                ('description', models.TextField(blank=True, max_length=600)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('name', models.CharField(max_length=62, primary_key=True, serialize=False, unique=True, validators=[WEB_SERVER.models.validator_name])),
            ],
        ),
        migrations.CreateModel(
            name='UserDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24)),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('join_time', models.DateTimeField(auto_now_add=True)),
                ('last_activate', models.DateTimeField(blank=True, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='UserDevice', to='WEB_SERVER.device')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AUTH_SYSTEM.permissions_group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='UserDevice', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Source_Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.FloatField(max_length=12)),
                ('source', models.FileField(upload_to='sources')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WEB_SERVER.type')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WEB_SERVER.type'),
        ),
        migrations.AddField(
            model_name='device',
            name='users',
            field=models.ManyToManyField(related_name='devices', through='WEB_SERVER.UserDevice', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Data_Device', to='WEB_SERVER.device')),
            ],
        ),
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('ًCS', 'Command Server'), ('CU', 'Command User')], max_length=20)),
                ('command', models.JSONField()),
                ('status', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('time_completed', models.DateTimeField(blank=True, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Command_Device', to='WEB_SERVER.device')),
            ],
        ),
        migrations.CreateModel(
            name='Button',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('control_name', models.CharField(max_length=80)),
                ('name', models.CharField(max_length=80)),
                ('array', models.TextField()),
                ('is_star', models.BooleanField(default=False)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WEB_SERVER.device')),
            ],
        ),
        migrations.AddConstraint(
            model_name='userdevice',
            constraint=models.UniqueConstraint(fields=('user', 'device'), name='unique_field_userdevice'),
        ),
    ]
