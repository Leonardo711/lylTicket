# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-11-10 14:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trainManage', '0005_auto_20161110_0644'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carriage',
            fields=[
                ('carriage_key', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('carriage_id', models.IntegerField(default=1)),
                ('num_seat', models.IntegerField(default=0)),
                ('seat_type', models.CharField(max_length=10)),
                ('train_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainManage.Train')),
            ],
        ),
        migrations.RemoveField(
            model_name='seat',
            name='carriage_id',
        ),
        migrations.RemoveField(
            model_name='seat',
            name='seat_type',
        ),
        migrations.RemoveField(
            model_name='seat',
            name='train_id',
        ),
        migrations.AddField(
            model_name='seat',
            name='carriage',
            field=models.ForeignKey(default='abc', on_delete=django.db.models.deletion.CASCADE, to='trainManage.Carriage'),
            preserve_default=False,
        ),
    ]
