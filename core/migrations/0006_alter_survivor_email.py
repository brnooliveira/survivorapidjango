# Generated by Django 4.2 on 2023-04-07 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_survivor_nickname_alter_survivor_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survivor',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]