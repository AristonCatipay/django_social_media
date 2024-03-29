# Generated by Django 5.0.1 on 2024-02-10 11:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
        ('user_profile', '0003_alter_profile_gender_follow_delete_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='barangay',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='address.barangay'),
        ),
        migrations.AddField(
            model_name='profile',
            name='city_municipality',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='address.city_municipality'),
        ),
        migrations.AddField(
            model_name='profile',
            name='province',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='address.province'),
        ),
        migrations.AddField(
            model_name='profile',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='address.region'),
        ),
    ]
