# Generated by Django 4.2 on 2023-05-03 08:02

from django.db import migrations, models
import uploadvideofile.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to='videosdatabase', validators=[uploadvideofile.models.Media.validate_file_extension])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('video_id', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('duration', models.CharField(max_length=100)),
                ('iframe', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
    ]