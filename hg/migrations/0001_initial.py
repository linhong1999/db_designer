# Generated by Django 2.2.6 on 2020-01-01 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('yhn', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('sNo', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('sName', models.CharField(max_length=20)),
                ('sSex', models.CharField(choices=[('0', 'female'), ('1', 'male')], max_length=10)),
                ('sYear', models.CharField(max_length=20, null=True)),
                ('sD', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yhn.Depart')),
                ('sDM', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yhn.DepartMajor')),
                ('s_mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yhn.TeacherInfo')),
            ],
            options={
                'db_table': 'Student',
            },
        ),
        migrations.CreateModel(
            name='StudentClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scNo', models.CharField(max_length=20)),
                ('scD', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yhn.Depart')),
                ('scDM', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yhn.DepartMajor')),
                ('scSNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hg.Student')),
            ],
            options={
                'db_table': 'StudentClass',
            },
        ),
    ]
