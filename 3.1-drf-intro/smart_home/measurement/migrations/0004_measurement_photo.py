# Generated by Django 4.1.3 on 2022-11-22 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0003_alter_measurement_temperature_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]