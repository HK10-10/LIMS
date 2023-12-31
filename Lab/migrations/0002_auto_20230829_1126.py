# Generated by Django 3.1.2 on 2023-08-29 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Lab', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('value', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='bill',
            name='test_name',
        ),
        migrations.DeleteModel(
            name='Report',
        ),
        migrations.AddField(
            model_name='test',
            name='bill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Lab.bill'),
        ),
        migrations.AddField(
            model_name='patient',
            name='tests',
            field=models.ManyToManyField(to='Lab.Test'),
        ),
    ]
