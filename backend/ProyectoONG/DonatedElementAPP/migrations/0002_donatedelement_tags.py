# Generated by Django 3.2.6 on 2021-11-01 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TagAPP', '0001_initial'),
        ('DonatedElementAPP', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='donatedelement',
            name='tags',
            field=models.ManyToManyField(to='TagAPP.Tag'),
        ),
    ]