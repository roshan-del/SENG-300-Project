# Generated by Django 3.0.5 on 2020-04-15 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papers', '0016_auto_20200414_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='papers',
            name='preferred_reviewers',
            field=models.CharField(default='', max_length=1000),
        ),
    ]