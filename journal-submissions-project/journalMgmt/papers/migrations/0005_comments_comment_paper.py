# Generated by Django 3.0.4 on 2020-04-03 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('papers', '0004_auto_20200329_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='comment_paper',
            field=models.ForeignKey(default='4', on_delete=django.db.models.deletion.CASCADE, to='papers.Papers'),
        ),
    ]
