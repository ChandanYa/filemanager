# Generated by Django 5.1.7 on 2025-03-27 16:53

import core.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=core.models.user_directory_path)),
                ('original_filename', models.CharField(max_length=255)),
                ('file_type', models.CharField(choices=[('PDF', 'PDF'), ('EXCEL', 'Excel'), ('WORD', 'Word'), ('TXT', 'Text'), ('OTHER', 'Other')], max_length=10)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
