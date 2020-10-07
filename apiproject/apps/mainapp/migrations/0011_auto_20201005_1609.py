# Generated by Django 3.1.1 on 2020-10-05 16:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_photo_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='thumbnail',
            field=models.ImageField(upload_to='thumbnail_photos', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]),
        ),
    ]
