# Generated by Django 2.0.3 on 2018-08-03 21:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_task_taskstatus_taskstepstatus'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskstatus',
            options={'verbose_name_plural': 'Task Statuses'},
        ),
        migrations.AlterModelOptions(
            name='taskstepstatus',
            options={'verbose_name_plural': 'Task Step Statuses'},
        ),
    ]
