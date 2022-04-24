# Generated by Django 3.2.13 on 2022-04-24 10:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='restaurant',
        ),
        migrations.AddField(
            model_name='menu',
            name='upload_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Upload Date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vote',
            name='menu',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='voting.menu', verbose_name='Menu'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vote',
            name='voting_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Voting Date'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='contact_no',
            field=models.CharField(blank=True, default='', max_length=24, verbose_name='Contact No'),
        ),
        migrations.AddConstraint(
            model_name='menu',
            constraint=models.UniqueConstraint(fields=('restaurant', 'upload_date'), name='unique_restaurant_menu_per_day'),
        ),
        migrations.AddConstraint(
            model_name='vote',
            constraint=models.UniqueConstraint(fields=('employee', 'voting_date'), name='unique_employee_vote_per_day'),
        ),
    ]