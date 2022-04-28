# Generated by Django 3.2.13 on 2022-04-28 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.SmallIntegerField(choices=[(1, 'Admin'), (2, 'Employee'), (3, 'Restaurant_owner')], default=1, verbose_name='User Type'),
        ),
    ]
