# Generated by Django 4.2.5 on 2023-11-05 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0002_metadata_reciever_alter_metadata_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='metadata',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metadata', to='messenger.metadata'),
        ),
    ]
