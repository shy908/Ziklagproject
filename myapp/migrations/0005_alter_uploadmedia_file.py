# Generated by Django 4.2.1 on 2023-06-23 19:36

from django.db import migrations, models
import myapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_uploadmedia_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadmedia',
            name='file',
            field=models.FileField(upload_to=myapp.models.media_upload_path),
        ),
    ]