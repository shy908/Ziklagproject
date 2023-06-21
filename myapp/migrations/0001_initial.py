# Generated by Django 4.2.1 on 2023-06-12 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('description', models.TextField()),
                ('file', models.TextField()),
                ('media_type', models.CharField(choices=[('video', 'Video'), ('audio', 'Audio'), ('image', 'Image'), ('file', 'File')], default='file', max_length=10)),
            ],
            options={
                'db_table': 'myapp_media',
            },
        ),
    ]