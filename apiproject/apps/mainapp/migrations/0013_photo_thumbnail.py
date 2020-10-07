# Generated by Django 3.1.1 on 2020-10-05 16:42

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_remove_photo_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='thumbnail',
            field=imagekit.models.fields.ProcessedImageField(default='', upload_to='thumbnails'),
        ),
    ]
