# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-10 20:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('key', models.CharField(max_length=100)),
                ('ad_site', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Advertiser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('fb_id', models.CharField(max_length=250, unique=True)),
                ('gender', models.CharField(max_length=20, null=True)),
                ('last_logged_in_at', models.DateTimeField(auto_now=True)),
                ('latitude', models.CharField(max_length=100)),
                ('longitude', models.CharField(max_length=100)),
                ('area', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('country', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserAdvertisementViewed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view_start_at', models.DateTimeField(auto_now_add=True)),
                ('view_end_at', models.DateTimeField(null=True)),
                ('advertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appStuff.Advertisement')),
                ('app_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appStuff.AppUser')),
            ],
        ),
        migrations.AddField(
            model_name='advertisement',
            name='advertiser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appStuff.Advertiser'),
        ),
    ]
