# Generated by Django 2.2.2 on 2019-06-25 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_diet', '0002_auto_20190625_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat',
            name='diet',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
