# Generated by Django 2.2.7 on 2019-11-07 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UserManager', '0005_admin_coordinator_event_head_publicity_volunteer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.AutoField(primary_key=True, serialize=False)),
                ('event_name', models.CharField(max_length=50)),
                ('Evnet_Detail', models.TextField()),
                ('rules', models.TextField()),
                ('event_logo', models.ImageField(null=True, upload_to='event_logo')),
                ('event_status', models.CharField(choices=[('Available', 'Available'), ('Scrapped', 'Scrapped'), ('Delete', 'Delete')], max_length=30)),
                ('venue', models.CharField(max_length=50)),
                ('date_time', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='news',
            fields=[
                ('news_id', models.AutoField(primary_key=True, serialize=False)),
                ('for_whome', models.CharField(choices=[('Participants', 'Participants'), ('Volunteer', 'Volunteer')], max_length=50)),
                ('news_containt', models.TextField()),
                ('hyperlink', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Parent_event',
            fields=[
                ('parent_event_id', models.AutoField(primary_key=True, serialize=False)),
                ('parent_event_name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Registers',
            fields=[
                ('reg_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('remark', models.TextField()),
                ('total_payment', models.IntegerField()),
                ('remaining_payment', models.IntegerField()),
                ('paid_payment', models.IntegerField()),
                ('conformed', models.BooleanField(default=False)),
                ('is_paid', models.BooleanField(default=False)),
                ('filled_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='UserManager.Publicity_Volunteer')),
            ],
        ),
        migrations.CreateModel(
            name='Winner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(choices=[('1', 'First'), ('2', 'Second'), ('3', 'Third')])),
                ('winning_certificate_issue', models.BooleanField(default=False)),
                ('certi_otp', models.IntegerField()),
                ('event_head_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='UserManager.Event_Head')),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EventWebSite.Event')),
                ('winner_reg_no', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='EventWebSite.Registers')),
            ],
        ),
        migrations.CreateModel(
            name='vol_to_admin_pay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('date_time', models.DateTimeField()),
                ('a_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='UserManager.Admin')),
                ('vol_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='UserManager.Event_Commitee')),
            ],
        ),
        migrations.CreateModel(
            name='to_whome_paid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('date_time', models.DateTimeField()),
                ('reg_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EventWebSite.Registers')),
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
                ('done_by', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='UserManager.Event_Commitee')),
            ],
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_status', models.CharField(choices=[('Not_paid', 'Not Paid'), ('Paid', 'Paid'), ('Comform', 'Conform'), ('Attended', 'Attended'), ('Certificate_issued', 'Certificate Issued'), ('Attended_winner', 'Attended Winner'), ('Scrapped', 'Scrapped'), ('Delete', 'Delete')], max_length=50)),
                ('certi_otp', models.IntegerField()),
                ('event_attendance_qr', models.ImageField(upload_to='event_attendance_qr')),
                ('amount', models.IntegerField()),
                ('event_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='EventWebSite.Event')),
                ('reg_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EventWebSite.Registers')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='parent_event',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='EventWebSite.Parent_event'),
        ),
    ]