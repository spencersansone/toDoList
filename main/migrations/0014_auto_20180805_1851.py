# Generated by Django 2.0.3 on 2018-08-05 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0013_auto_20180805_1851'),
    ]

    operations = [
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('step_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='StepEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField()),
                ('due_datetime', models.DateTimeField()),
                ('completed', models.BooleanField()),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Step')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('routine_task', models.BooleanField()),
                ('sunday', models.BooleanField()),
                ('monday', models.BooleanField()),
                ('tuesday', models.BooleanField()),
                ('wednesday', models.BooleanField()),
                ('thursday', models.BooleanField()),
                ('friday', models.BooleanField()),
                ('saturday', models.BooleanField()),
                ('certain_due_date_task', models.BooleanField()),
                ('date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField()),
                ('due_datetime', models.DateTimeField(blank=True, null=True)),
                ('completed', models.BooleanField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Task')),
            ],
        ),
        migrations.AddField(
            model_name='stepentry',
            name='task_entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.TaskEntry'),
        ),
        migrations.AddField(
            model_name='step',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Task'),
        ),
    ]