# Generated by Django 4.1.3 on 2023-01-19 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phoneno',
            field=models.IntegerField(),
        ),
    ]
