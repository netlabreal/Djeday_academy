# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-13 02:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djedayApp', '0003_auto_20170513_1042'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidates',
            options={'ordering': ['name'], 'verbose_name': 'кандидат', 'verbose_name_plural': 'кандидаты'},
        ),
        migrations.AlterModelOptions(
            name='djeday',
            options={'ordering': ['name'], 'verbose_name': 'джедай', 'verbose_name_plural': 'джедаи'},
        ),
        migrations.AlterModelOptions(
            name='planet',
            options={'ordering': ['name'], 'verbose_name': 'планета', 'verbose_name_plural': 'планеты'},
        ),
        migrations.AlterModelOptions(
            name='spisokvoprosov',
            options={'ordering': ['code'], 'verbose_name': 'список вопросов', 'verbose_name_plural': 'список вопросов'},
        ),
        migrations.AlterModelOptions(
            name='voprosi',
            options={'ordering': ['naim'], 'verbose_name': 'вопрос', 'verbose_name_plural': 'вопросы'},
        ),
        migrations.RenameField(
            model_name='spisokvoprosov',
            old_name='name',
            new_name='code',
        ),
        migrations.AddField(
            model_name='candidates',
            name='master',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='djedayApp.Djeday'),
        ),
        migrations.AddField(
            model_name='voprosi',
            name='code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='djedayApp.SpisokVoprosov'),
        ),
        migrations.AddField(
            model_name='voprosi',
            name='naim',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='candidates',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='voprosi',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
