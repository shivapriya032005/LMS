# Generated by Django 5.0.6 on 2024-07-07 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0018_pdfdocument'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentextra',
            name='enrollment',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]
