# Generated by Django 3.1.1 on 2020-09-29 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20200928_1457'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='picture',
            new_name='file',
        ),
        migrations.AlterField(
            model_name='album',
            name='album_name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]