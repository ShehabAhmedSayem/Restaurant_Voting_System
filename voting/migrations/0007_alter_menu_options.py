# Generated by Django 3.2.13 on 2022-04-26 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0006_restaurant_winning_streak'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={'ordering': ['-num_of_votes', 'id'], 'verbose_name': 'Menu', 'verbose_name_plural': 'Menus'},
        ),
    ]
