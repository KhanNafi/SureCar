# Generated by Django 4.0.3 on 2022-04-16 17:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_rename_buyer_id_wants_buyer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wants',
            name='buyer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
