# Generated by Django 3.2.9 on 2021-11-18 08:48
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("survey", "1002_auto_20211117_1602"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recommendations",
            name="label",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="surveyquestion",
            name="label",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="surveyquestionanswer",
            name="label",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="surveyquestionservicecategory",
            name="label",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="surveysection",
            name="label",
            field=models.TextField(),
        ),
    ]
