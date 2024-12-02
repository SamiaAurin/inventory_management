# Generated by Django 4.2.7 on 2024-12-03 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0002_partition_localize_accommodation'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='localizeaccommodation',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='localizeaccommodation',
            constraint=models.UniqueConstraint(fields=('property', 'language'), name='unique_property_language'),
        ),
    ]
