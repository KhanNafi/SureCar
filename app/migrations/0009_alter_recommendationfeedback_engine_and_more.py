# Generated by Django 4.0.3 on 2022-04-17 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_recommendationfeedback_delete_buyer_delete_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendationfeedback',
            name='engine',
            field=models.DecimalField(decimal_places=5, max_digits=9),
        ),
        migrations.AlterField(
            model_name='recommendationfeedback',
            name='km_driven',
            field=models.DecimalField(decimal_places=5, max_digits=9),
        ),
        migrations.AlterField(
            model_name='recommendationfeedback',
            name='mileage',
            field=models.DecimalField(decimal_places=5, max_digits=9),
        ),
        migrations.AlterField(
            model_name='recommendationfeedback',
            name='price',
            field=models.DecimalField(decimal_places=5, max_digits=9),
        ),
        migrations.AlterField(
            model_name='recommendationfeedback',
            name='year',
            field=models.DecimalField(decimal_places=5, max_digits=9),
        ),
    ]