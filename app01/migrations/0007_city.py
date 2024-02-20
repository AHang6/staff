# Generated by Django 4.2.9 on 2024-01-31 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_alter_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='用户名')),
                ('count', models.IntegerField(verbose_name='人口')),
                ('img', models.FileField(max_length=128, upload_to='', verbose_name='LOGO')),
            ],
        ),
    ]
