# Generated by Django 3.2.6 on 2021-11-04 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DonationAPP', '0001_initial'),
        ('DonatedElementAPP', '0002_donatedelement_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='donatedelement',
            name='donation',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='DonationAPP.donation'),
        ),
    ]
