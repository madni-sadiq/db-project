# Generated by Django 3.1.5 on 2021-01-15 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Frozery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=15)),
                ('Last_name', models.CharField(max_length=15)),
                ('phoneno', models.CharField(max_length=11)),
                ('addr', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=500)),
            ],
        ),
    ]
