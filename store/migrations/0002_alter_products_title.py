# Generated by Django 4.0.2 on 2022-11-26 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='title',
            field=models.CharField(default='', max_length=100),
        ),
    ]