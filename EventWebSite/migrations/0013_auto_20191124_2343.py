# Generated by Django 2.2.7 on 2019-11-24 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserManager', '0015_admin_coordinator_event_head_volunteer'),
        ('EventWebSite', '0012_auto_20191124_2340'),
    ]

    operations = [
        migrations.AddField(
            model_name='registers',
            name='filled_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='UserManager.Volunteer'),
        ),
        migrations.AddField(
            model_name='sponsers',
            name='done_by',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='UserManager.Event_Committee'),
        ),
        migrations.AddField(
            model_name='winner',
            name='event_head_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='UserManager.Event_Head'),
        ),
        migrations.CreateModel(
            name='vol_to_admin_pay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('date_time', models.DateTimeField()),
                ('a_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='UserManager.Admin')),
                ('vol_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='UserManager.Event_Committee')),
            ],
        ),
    ]