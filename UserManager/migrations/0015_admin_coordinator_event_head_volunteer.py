# Generated by Django 2.2.7 on 2019-11-24 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserManager', '0014_event_committee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('reg_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='UserManager.Event_Committee')),
                ('isActive', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Coordinator',
            fields=[
                ('reg_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='UserManager.Event_Committee')),
                ('payment_hold', models.IntegerField()),
                ('isActive', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Event_Head',
            fields=[
                ('reg_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='UserManager.Event_Committee')),
                ('isActive', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('reg_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='UserManager.Event_Committee')),
                ('payment_hold', models.IntegerField(default=0)),
                ('isActive', models.BooleanField(default=False)),
            ],
        ),
    ]