# Generated by Django 2.2.7 on 2019-11-07 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManager', '0003_event_commitee_participant'),
    ]

    operations = [
        migrations.AddField(
            model_name='event_commitee',
            name='commitee_id',
            field=models.CharField(default='17bce000', max_length=20, unique=True),
            preserve_default=False,
        ),
    ]