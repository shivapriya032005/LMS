# Generated by Django 5.0.6 on 2024-07-04 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0014_remove_book_name_book_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(default='Untitled Book', max_length=200),
        ),
    ]
