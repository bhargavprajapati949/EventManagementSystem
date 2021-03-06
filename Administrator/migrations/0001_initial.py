# Generated by Django 3.0 on 2019-12-13 19:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('EventWebSite', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UserManager', '0004_volunteer'),
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
            name='vol_to_admin_pay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('date_time', models.DateTimeField()),
                ('a_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='Administrator.Admin')),
                ('vol_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='UserManager.Event_Committee')),
            ],
        ),
        migrations.CreateModel(
            name='to_whome_paid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('date_time', models.DateTimeField()),
                ('reg_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EventWebSite.Participants')),
                ('to_paid', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sponsers',
            fields=[
                ('s_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('logo', models.ImageField(upload_to='sponsers_logo')),
                ('amount', models.IntegerField(null=True)),
                ('date', models.DateField()),
                ('done_by', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='UserManager.Event_Committee')),
            ],
        ),
    ]
