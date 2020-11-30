# Generated by Django 3.1.3 on 2020-11-29 11:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Reservation', '0002_auto_20201129_1125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='guest',
        ),
        migrations.RemoveField(
            model_name='service',
            name='is_paid',
        ),
        migrations.CreateModel(
            name='UserServices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField(default=False)),
                ('guest', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Reservation.service')),
            ],
        ),
    ]