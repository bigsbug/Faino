# Generated by Django 3.2.5 on 2021-07-11 11:05

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=36)),
                ('description', models.TextField(blank=True, max_length=600)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('name', models.CharField(max_length=36)),
                ('phone', models.CharField(max_length=11)),
                ('company', models.CharField(blank=True, max_length=60)),
                ('membership', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('name', models.CharField(max_length=62, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewStatus',
            fields=[
                ('device', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='New_Status_Device', serialize=False, to='Demo_webserver_app.device')),
                ('data', models.JSONField()),
                ('complated', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Demo_webserver_app.type'),
        ),
        migrations.AddField(
            model_name='device',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Device_user', to='Demo_webserver_app.profile'),
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Data_Device', to='Demo_webserver_app.device')),
            ],
        ),
    ]