# Generated by Django 2.0.3 on 2018-03-24 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ToolrAPI', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='google_id',
            field=models.TextField(primary_key=True, serialize=False),
        ),
    ]
