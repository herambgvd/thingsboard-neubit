# Generated by Django 4.2.16 on 2025-05-02 07:08

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_initial'),
        ('settings', '0002_alter_iotconfig_options_iotconfig_refresh_token_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamProfileImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('image', models.ImageField(upload_to='team_profile_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.team', verbose_name='Team')),
            ],
            options={
                'verbose_name': 'Team Profile Image',
                'verbose_name_plural': 'Team Profile Images',
            },
        ),
    ]
