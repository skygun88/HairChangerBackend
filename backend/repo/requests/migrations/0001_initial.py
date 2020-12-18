# Generated by Django 3.1.3 on 2020-11-09 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RequestInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=20)),
                ('rid', models.CharField(max_length=20, unique=True)),
                ('facePath', models.CharField(max_length=50)),
                ('hairPath', models.CharField(max_length=50)),
                ('convertedPath', models.CharField(max_length=50)),
                ('progress', models.IntegerField(default=0)),
            ],
        ),
    ]
