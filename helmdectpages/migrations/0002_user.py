# Generated by Django 4.2.7 on 2023-11-25 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helmdectpages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('confirm_password', models.CharField(max_length=100)),
            ],
        ),
    ]
