# Generated by Django 4.2.9 on 2024-01-26 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.SmallIntegerField(choices=[(1, '待支付'), (2, '已支付')], default=1, verbose_name='状态'),
        ),
    ]
