# Generated by Django 3.1.3 on 2020-12-04 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0004_auto_20201204_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestinfo',
            name='rid',
            field=models.IntegerField(default=0),
        ),
    ]
