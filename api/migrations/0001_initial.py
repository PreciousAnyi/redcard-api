# Generated by Django 4.2.13 on 2024-07-15 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=100)),
                ('points', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RedCard',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('issued_at', models.DateTimeField(auto_now_add=True)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.card')),
                ('issued_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.invigilator')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.student')),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('invigilators', models.ManyToManyField(to='user_management.invigilator')),
            ],
        ),
        migrations.CreateModel(
            name='Blacklist',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('student_name', models.CharField(editable=False, max_length=100)),
                ('threshold', models.IntegerField(editable=False)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user_management.student')),
            ],
        ),
    ]