# Generated by Django 3.2.6 on 2021-11-12 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TagAPP', '0001_initial'),
        ('DonatedElementAPP', '0005_alter_donatedelement_donation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donatedelement',
            name='tags',
            field=models.ManyToManyField(related_name='tags', to='TagAPP.Tag'),
        ),
    ]
