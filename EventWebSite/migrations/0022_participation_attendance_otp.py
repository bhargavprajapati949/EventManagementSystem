# Generated by Django 2.2.7 on 2019-11-26 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventWebSite', '0021_auto_20191127_0129'),
    ]

    operations = [
        migrations.AddField(
            model_name='participation',
            name='attendance_otp',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
