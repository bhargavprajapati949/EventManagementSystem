# Generated by Django 2.2.7 on 2019-11-20 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserManager', '0006_auto_20191121_0053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='clg_id',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='UserManager.Collages', verbose_name='Collage'),
        ),
        migrations.AlterField(
            model_name='user',
            name='contect_no',
            field=models.IntegerField(verbose_name='Contect No'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='fname',
            field=models.CharField(max_length=50, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_participant',
            field=models.BooleanField(default=False, verbose_name='Participant'),
        ),
        migrations.AlterField(
            model_name='user',
            name='lname',
            field=models.CharField(max_length=50, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='reg_no',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='Registration Number'),
        ),
        migrations.AlterField(
            model_name='user',
            name='stream',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='UserManager.Stream', verbose_name='Stream'),
        ),
    ]
