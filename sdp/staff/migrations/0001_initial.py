# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-30 03:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HumanResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=8)),
                ('password', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='participant',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.Staff'),
        ),
        migrations.AddField(
            model_name='instructor',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.Staff'),
        ),
        migrations.AddField(
            model_name='humanresource',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.Staff'),
        ),
        migrations.AddField(
            model_name='administrator',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.Staff'),
        ),
    ]
