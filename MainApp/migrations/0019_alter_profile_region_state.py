# Generated by Django 5.2.1 on 2025-06-03 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0018_alter_profile_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='region_state',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
