# Generated by Django 2.0 on 2018-04-18 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ToolrAPI', '0017_auto_20180418_0104'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='isProposal',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='proposal',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='proposal', to='ToolrAPI.Loan'),
        ),
    ]
