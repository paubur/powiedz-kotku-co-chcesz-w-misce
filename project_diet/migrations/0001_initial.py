# Generated by Django 2.2.2 on 2019-06-25 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('age', models.IntegerField()),
                ('birthmark', models.CharField(max_length=255)),
                ('medical_condition', models.TextField()),
                ('diet', models.BooleanField(default=False)),
                ('diet_description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Composition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=255)),
                ('cat', models.ManyToManyField(to='project_diet.Cat')),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('composition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_diet.Composition')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_diet.Food')),
            ],
        ),
        migrations.AddField(
            model_name='composition',
            name='food',
            field=models.ManyToManyField(through='project_diet.Content', to='project_diet.Food'),
        ),
    ]