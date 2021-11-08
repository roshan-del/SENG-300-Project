# Generated by Django 3.0.4 on 2020-04-10 17:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('papers', '0007_auto_20200409_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='papers',
            name='paper_reviewer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paper_reviewed_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='papers',
            name='paper_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paper_written_by', to=settings.AUTH_USER_MODEL),
        ),
    ]