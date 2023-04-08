# Generated by Django 4.2 on 2023-04-07 05:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_survivor_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survivor',
            name='nickname',
        ),
        migrations.AlterField(
            model_name='survivor',
            name='username',
            field=models.CharField(blank=True, help_text='Survivor Name', max_length=50, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(5)], verbose_name='Name'),
        ),
    ]
