# Generated by Django 2.2.6 on 2020-01-01 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('yhn', '0001_initial'),
        ('hg', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cName', models.CharField(max_length=20)),
                ('cTerm', models.CharField(max_length=20)),
                ('cCapacity', models.CharField(max_length=3)),
                ('cType', models.CharField(choices=[('0', 'A'), ('1', 'B'), ('2', 'C'), ('3', 'D')], max_length=10)),
                ('cScore', models.CharField(max_length=10)),
                ('cDepart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yhn.Depart')),
                ('cDepartMajor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yhn.DepartMajor')),
                ('cNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yhn.CourseInfo')),
                ('cStudent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hg.Student')),
                ('cTeacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yhn.TeacherInfo')),
            ],
            options={
                'db_table': 'Course',
            },
        ),
    ]
