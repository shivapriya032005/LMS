# Generated by Django 5.0.6 on 2024-07-04 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0015_alter_book_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='title',
            new_name='name',
        ),
    ]
