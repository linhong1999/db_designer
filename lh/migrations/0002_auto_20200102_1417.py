# Generated by Django 2.2.6 on 2020-01-02 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lh', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operatelog',
            name='review_status',
            field=models.CharField(choices=[('0', '默认'), ('1', '通过'), ('2', '未通过')], default='0', max_length=10),
        ),
    ]
