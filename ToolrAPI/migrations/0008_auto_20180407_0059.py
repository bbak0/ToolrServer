# Generated by Django 2.0 on 2018-04-06 22:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ToolrAPI', '0007_auto_20180405_0439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='tool',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='picture', to='ToolrAPI.Tool'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='google_id',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]