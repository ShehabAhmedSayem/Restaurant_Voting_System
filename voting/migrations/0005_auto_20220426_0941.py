# Generated by Django 3.2.13 on 2022-04-26 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0004_auto_20220426_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='is_voting_stopped',
            field=models.BooleanField(default=False, verbose_name='Is Voting Stopped'),
        ),
        migrations.AlterField(
            model_name='result',
            name='voting_date',
            field=models.DateField(unique=True, verbose_name='Voting Date'),
        ),
        migrations.AlterField(
            model_name='result',
            name='winning_menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='results', to='voting.menu', verbose_name='Winning Menu'),
        ),
    ]
