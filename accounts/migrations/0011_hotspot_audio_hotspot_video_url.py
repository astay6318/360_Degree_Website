# Generated by Django 4.2.4 on 2024-03-03 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_scene_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotspot',
            name='audio',
            field=models.FileField(blank=True, null=True, upload_to='hotspot_audios/'),
        ),
        migrations.AddField(
            model_name='hotspot',
            name='video_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
