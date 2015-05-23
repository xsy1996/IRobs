# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Desk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.IPAddressField()),
                ('num', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('price', models.FloatField()),
                ('typ', models.CharField(max_length=128)),
                ('intro', models.TextField()),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'photos')),
                ('intro', models.TextField()),
                ('dish', models.ForeignKey(to='Client.Dish')),
            ],
        ),
        migrations.CreateModel(
            name='Myuser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permission', models.IntegerField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('paied', models.IntegerField()),
                ('pub_date', models.DateField()),
                ('desk', models.ForeignKey(to='Client.Desk')),
                ('dish', models.ManyToManyField(to='Client.Dish')),
            ],
        ),
        migrations.CreateModel(
            name='Remark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('pub_date', models.DateField()),
                ('client', models.ForeignKey(to='Client.Myuser')),
                ('dish', models.ForeignKey(to='Client.Dish')),
            ],
        ),
    ]
