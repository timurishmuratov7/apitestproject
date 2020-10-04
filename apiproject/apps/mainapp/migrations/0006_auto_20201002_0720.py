# Generated by Django 3.1.1 on 2020-10-02 07:20

import django.core.validators
from django.db import migrations, models
import mainapp.validators
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('mainapp', '0005_auto_20200929_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(upload_to='photos', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']), mainapp.validators.file_size_validator]),
        ),
        migrations.AlterField(
            model_name='photo',
            name='photo_name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
