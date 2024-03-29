# Generated by Django 4.2.11 on 2024-03-10 06:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shorts', models.CharField(db_index=True, max_length=16, unique=True, verbose_name='短链接字符')),
                ('target', models.URLField(max_length=256, verbose_name='长链接')),
                ('create_at', models.DateTimeField(verbose_name='创建时间')),
                ('expire_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='过期时间')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                              verbose_name='创建者')),
            ],
            options={
                'db_table': 'core_short_link',
            },
        ),
    ]
