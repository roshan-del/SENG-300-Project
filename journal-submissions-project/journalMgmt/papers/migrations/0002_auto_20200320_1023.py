# Generated by Django 3.0.4 on 2020-03-20 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='papers',
            name='paper_file',
            field=models.FileField(upload_to='papers/'),
        ),
    ]
