# Generated by Django 4.2.1 on 2023-05-30 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploadvideofile', '0010_alter_uploader_fb_access_key_alter_uploader_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploader',
            old_name='reddit_password',
            new_name='subreddit',
        ),
        migrations.RemoveField(
            model_name='uploader',
            name='reddit_user',
        ),
        migrations.AlterField(
            model_name='uploader',
            name='fb_access_key',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]