# Generated by Django 3.0.4 on 2020-04-09 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papers', '0005_comments_comment_paper'),
    ]

    operations = [
        migrations.AddField(
            model_name='papers',
            name='paper_status',
            field=models.CharField(max_length=255, null=True),
        ),
    ]