# Generated by Django 4.2.1 on 2023-06-14 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_uploadmedia_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadmedia',
            name='file',
            field=models.TextField(),
        ),
    ]