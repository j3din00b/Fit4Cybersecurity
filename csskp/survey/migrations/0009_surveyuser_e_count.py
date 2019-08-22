# Generated by Django 2.2.3 on 2019-08-22 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0008_auto_20190813_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyuser',
            name='e_count',
            field=models.CharField(choices=[(0, '1-5'), (1, '6-10'), (2, '10-20'), (3, '20-50'), (4, '50-100'), (5, '100-200'), (6, '200-500'), (7, '500-1000'), (7, '1000-5000'), (7, '5000+')], default=0, max_length=2),
        ),
    ]