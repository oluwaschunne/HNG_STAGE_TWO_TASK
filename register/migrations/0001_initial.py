# Generated by Django 5.0.6 on 2024-07-08 22:22

import register.utils
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('userId', models.CharField(default=register.utils.generate_uuid, editable=False, max_length=36, unique=True)),
                ('firstName', models.CharField(max_length=30)),
                ('lastName', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('users', models.ManyToManyField(related_name='organisations', to='register.user')),
            ],
        ),
    ]
